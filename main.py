from diracdec.theory.typeddirac import *

if __name__ == "__main__":

    print(signature.cime2_repr())
    # print(type_checker.cime_vars_repr())
    # print(type_checker.cime_trs_repr())
    print(typed_trs.cime_vars_repr())

    # print(typed_trs.original_rules_repr())

    print(typed_trs.cime_trs_repr())    

    b = parse('''
              < s : U ^ V | 
              @ (
                    
                        (
                            (o1 : O(U, W)) & 
                            (o2 : O(V, R))
                        ) @ (k : K(W ^ R))
              )
              ''')
    # print(type_checker.normalize(b))

