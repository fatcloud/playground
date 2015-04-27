def func1(a, **kwargs):
    print 'func1:', kwargs['b']
    func2(**kwargs)
    
def func2(a=5,**kargs):
    print 'func2:', a
    print kargs

    
func1(a=7,b=60)