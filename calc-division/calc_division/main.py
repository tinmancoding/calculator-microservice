from calc_common import Calculation, Number, init_app, Operation, calc_fn


def division_fn(c: Calculation) -> Number:
    return calc_fn(c.left) / calc_fn(c.right)

        
app = init_app("division", {
    Operation.division:  division_fn
})

