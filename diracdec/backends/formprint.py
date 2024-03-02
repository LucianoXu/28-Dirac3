'''

formprint provides the standard and methods for pretty printing formulas

'''
from __future__ import annotations
from typing import Tuple, List

class FormBlock:
    def __init__(self, lines: Tuple[str, ...]):
        self._lines = lines

        self._height = len(lines)

        if len(lines) == 0:
            self._width = 0
        else:
            self._width = len(lines[0])
            if not all(len(line) == self._width for line in lines):
                raise ValueError('FormBlock: lines have different lengths')
            

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def is_empty(self) -> bool:
        return self._height == 0

    def __str__(self):
        return '\n'.join(self._lines)
    
class EmptyBlock(FormBlock):
    def __init__(self):
        super().__init__(())

    

class BaseBlock(FormBlock):
    def __init__(self, expr: str | FormBlock, 
                 width: None|int = None, 
                 height: None|int = None,
                 v_align: str = 'c',
                 h_align: str = 'c'):

        if isinstance(expr, FormBlock):
            expr = str(expr)

        if expr == '':
            super().__init__(())
            return

        # find the longest line of expr
        input_width = max(len(line) for line in expr.split('\n'))

        input_height = expr.count('\n') + 1

        if width is None:
            width = input_width

        if height is None:
            height = input_height

        if width < input_width or height < input_height:
            raise ValueError('BaseBlock: width or height too small')

        # calculate the padding according to the alignment

        if h_align == 'l':
            left_pad = 0
            right_pad = width - input_width
        elif h_align == 'r':
            right_pad = 0
            left_pad = width - input_width
        elif h_align == 'c':
            left_pad = (width - input_width) // 2
            right_pad = width - input_width - left_pad
        else:
            raise ValueError('BaseBlock: invalid h_align')
        
        if v_align == 't':
            up_pad = 0
            down_pad = height - input_height
        elif v_align == 'b':
            up_pad = height - input_height
            down_pad = 0
        elif v_align == 'c':
            up_pad = (height - input_height) // 2
            down_pad = height - input_height - up_pad
        else:
            raise ValueError('BaseBlock: invalid v_align')
        
        # first pad space to the right to get the same line width
        lines = tuple(
            line.ljust(input_width)
            for line in expr.split('\n'))

        # add padding to the right of each line
        lines = tuple(
            line.rjust(left_pad + input_width).ljust(width)
            for line in lines)
        
        # add padding to the top and bottom
        lines = (f'{" " * width}',) * up_pad + lines + (f'{" " * width}',) * down_pad

        super().__init__(lines)


class FrameBlock(FormBlock):
    def __init__(self, block: str|FormBlock, caption:str = ""):

        if isinstance(block, str):
            block = BaseBlock(block)

        self._block = block

        width = block._width + 2

        lines = tuple(
            f'│{line}│' for line in block._lines
        )
        if len(caption) > block._width:
            caption = caption[:block._width-3] + '...'

        lines = (f'{"┌" + caption + "─"*(width-len(caption)-2) + "┐"}', *lines, f'{"└" + "─"*(width-2) + "┘"}')

        super().__init__(lines)
        

class HSeqBlock(FormBlock):
    '''
    Horizontal Sequence Block
    '''
    def __init__(self, *blocks: FormBlock | str, v_align : str = 'c'):

        block_ls : List[FormBlock]= []

        for block in blocks:
            if isinstance(block, str):
                block_ls.append(BaseBlock(block))
            else:
                block_ls.append(block)

        # filter out empty blocks
        block_ls = [block for block in block_ls if not block.is_empty]

        self._block_ls = block_ls

        # check empty block
        if len(blocks) == 0:
            super().__init__(())
            return

        width = sum(block._width for block in block_ls)
        height = max(block._height for block in block_ls)

        # resize the blocks
        resized_blocks = [BaseBlock(block, block.width, height, v_align=v_align) for block in block_ls]

        # connect the lines
        zip_lines = zip(*[block._lines for block in resized_blocks])

        lines = tuple(''.join(line) for line in zip_lines)

        super().__init__(lines)


class VSeqBlock(FormBlock):
    '''
    Vertical Sequence Block
    '''
    def __init__(self, *blocks: FormBlock | str, h_align : str = 'c'):

        block_ls : List[FormBlock]= []

        for block in blocks:
            if isinstance(block, str):
                block_ls.append(BaseBlock(block))
            else:
                block_ls.append(block)

        # filter out empty blocks
        block_ls = [block for block in block_ls if not block.is_empty]

        self._block_ls = block_ls

        # check empty block
        if len(blocks) == 0:
            super().__init__(())
            return

        width = max(block._width for block in block_ls)
        height = sum(block._height for block in block_ls)

        # resize the blocks
        resized_blocks = [BaseBlock(block, width, block.height, h_align=h_align) for block in block_ls]

        # connect the lines
        lines = tuple(line for block in resized_blocks for line in block._lines)

        super().__init__(lines)

class IndexBlock(FormBlock):
    '''
    Block with 6 possible indices
    '''
    def __init__(self, body: str | FormBlock, 
                 UL_index: str | FormBlock | None = None,
                 U_index : str | FormBlock | None = None,
                 UR_index: str | FormBlock | None = None,
                 DL_index: str | FormBlock | None = None,
                 D_index : str | FormBlock | None = None,
                 DR_index: str | FormBlock | None = None):
        
        if isinstance(body, str):
            body = BaseBlock(body)
        if isinstance(UL_index, str):
            UL_index = BaseBlock(UL_index)
        if isinstance(U_index, str):
            U_index = BaseBlock(U_index)
        if isinstance(UR_index, str):
            UR_index = BaseBlock(UR_index)
        if isinstance(DL_index, str):
            DL_index = BaseBlock(DL_index)
        if isinstance(D_index, str):
            D_index = BaseBlock(D_index)
        if isinstance(DR_index, str):
            DR_index = BaseBlock(DR_index)

        self._body = body

        UL_width = 0 if UL_index is None else UL_index._width
        U_width = 0 if U_index is None else U_index._width
        UR_width = 0 if UR_index is None else UR_index._width
        DL_width = 0 if DL_index is None else DL_index._width
        D_width = 0 if D_index is None else D_index._width
        DR_width = 0 if DR_index is None else DR_index._width

        l_width = max(UL_width, DL_width)
        m_width = max(U_width, D_width, body._width)
        r_width = max(UR_width, DR_width)

        l_sep_needed = m_width > body._width - 2 and (UL_width > 0 or DL_width > 0)

        r_sep_needed = m_width > body._width - 2 and (DR_width > 0 or UR_width > 0)

        # calculate the width
        width = l_width + m_width + r_width
        if l_sep_needed:
            width += 1
        if r_sep_needed:
            width += 1 

        # arrange upper indices
        if UL_index is None and U_index is None and UR_index is None:
            u_blocks = EmptyBlock()
        else:
            u_blocks = []
            if UL_index is not None:
                u_blocks.append(BaseBlock(UL_index, width = l_width, h_align='r'))
            else:
                u_blocks.append(' '*l_width)

            if l_sep_needed:
                u_blocks.append(' ')

            if U_index is not None:
                u_blocks.append(BaseBlock(U_index, width = m_width, h_align='c'))
            else:
                u_blocks.append(' '*m_width)

            if r_sep_needed:
                u_blocks.append(' ')

            if UR_index is not None:
                u_blocks.append(BaseBlock(UR_index, width = r_width, h_align='l'))
            else:
                u_blocks.append(' '*r_width)

            u_blocks = HSeqBlock(*u_blocks, v_align='b')

        # arrange lower indices
        if DL_index is None and D_index is None and DR_index is None:
            d_blocks = EmptyBlock()
        else:
            d_blocks = []
            if DL_index is not None:
                d_blocks.append(BaseBlock(DL_index, width = l_width, h_align='r'))
            else:
                d_blocks.append(' '*l_width)
            
            if l_sep_needed:
                d_blocks.append(' ')

            if D_index is not None:
                d_blocks.append(BaseBlock(D_index, width = m_width, h_align='c'))
            else:
                d_blocks.append(' '*m_width)

            if r_sep_needed:
                d_blocks.append(' ')

            if DR_index is not None:
                d_blocks.append(BaseBlock(DR_index, width = r_width, h_align='l'))
            else:
                d_blocks.append(' '*r_width)

            d_blocks = HSeqBlock(*d_blocks, v_align='t')

        # arrange body block
        body_blocks = []
        body_blocks.append(BaseBlock(' ' * l_width, width = l_width))
        if l_sep_needed:
            body_blocks.append(' ')
        body_blocks.append(BaseBlock(body, width = m_width))
        if r_sep_needed:
            body_blocks.append(' ')
        body_blocks.append(BaseBlock(' ' * r_width, width = r_width))

        body_blocks = HSeqBlock(*body_blocks, v_align='c')

        final_block = VSeqBlock(
            u_blocks, 
            body_blocks,
            d_blocks, 
            h_align='c')

        super().__init__(final_block._lines)

class ParenBlock(FormBlock):
    '''
    Parentheses Block
    '''
    def __init__(self, block: str | FormBlock):
        if isinstance(block, str):
            block = BaseBlock(block)

        self._block = block
        
        if len(block._lines) == 1:
            lines = (f'({block._lines[0]})',)
        
        else:
            lines = (f'⎛{block._lines[0]}⎞',)
            lines += tuple(f'⎜{line}⎟' for line in block._lines[1:-1])
            lines += (f'⎝{block._lines[-1]}⎠',)

        super().__init__(lines)
