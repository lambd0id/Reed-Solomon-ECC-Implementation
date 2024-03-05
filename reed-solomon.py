#Error Correction Module
import io
import sys
def eea(a, p):
    t = 0
    next_t = 1
    p_orig = p
    while a>0:
        q = p//a
        r = p%a
        t = t-(q*next_t)
        t,next_t = next_t,t
        p = a
        a = r
    return t%p_orig

def add(a,b):
    return (a+b)%929
def multiply(a,b):
    return (a*b)%929
def subtract(a,b):
    return (a-b)%929
def divide(a,b):
    return (a*eea(b,929))%929
def power(a,x):
    n = a
    if x==0:
        return 1
    for i in range(x-1):
        n = multiply(n,a)
    return n

def syndromes(data,E,N,a_pow):
    s = [0]*E

    for i in range(E):
        n = 0
        for j in range(N):
            n = add(n,multiply(data[j],power(a_pow[i+1],N-1-j)))
        s[i] = n
    return s

def substitute(poly,n):
    ans = 0
    for i in range(len(poly)):
        ans = ans + multiply(poly[i],power(n,len(poly)-i-1))
    return ans%929

def ELP(s, E):
    L = [0]*E
    L[E-1] = 1
    ne = 0
    dp = 1
    Lp = list(L)
    m = 1
    d = 0
    
    for i in range(len(s)):
        d = s[i]
        for j in range(1,ne+1):
            d = add(d,multiply(L[-j-1],s[i-j]))
        if d==0:
            m += 1
        else:
            old_L = list(L)
            Lp_temp = list(Lp)
            for j in range(m):
                Lp_temp.append(0)
            Lp_temp = Lp_temp[m:]
            
            #L = (L - (divide(d,dp)*Lp_temp)%929)%929
            temp = []
            ddp = divide(d,dp)
            temp = [(ddp*x)%929 for x in Lp_temp]
            L = [a_i - b_i for a_i, b_i in zip(L, temp)]
            L = [x%929 for x in L]
            
            if (2*ne) <= i:
                Lp = list(old_L)
                ne = i+1-ne
                dp = d
                m = 1
            else:
                m += 1

    for j in range(len(L)):
        if not L[j]:
            pass
        else:
            L = L[j:]
            break
    return L

def chien(elp,a_pow,N):
    roots = []
    Le = list(elp)
    Le_len = len(Le)
    for i in range(929):
        elp_val = sum(Le)%929 #change
        if elp_val==0:
            roots = roots + [i]
        for j in range(Le_len):
            Le[j] = multiply(Le[j],a_pow[Le_len-1-j])
    to_remove = []
    for i in range(len(roots)):
        temp = (928 - roots[i])%929
        roots[i] = temp
        if temp > N:
            to_remove.append(i)
    for i in to_remove:
        roots.pop(i)
    roots.reverse()
    return roots


def eep(s,elp,roots,a_pow):
    elp_len = len(elp)
    DL = [0]*elp_len
    for i in range(elp_len):
        DL[i] = multiply(elp[i],elp_len-1-i)
    DL = DL[:len(DL)-1]

    O = [0]*(elp_len+len(s)-1)
    Ltemp = list(elp)
    Ltemp.reverse()

    for o1,i1 in enumerate(s):
        for o2,i2 in enumerate(Ltemp):
            O[o1+o2] = add(O[o1+o2],multiply(i1,i2))
    O = list(O[:elp_len-1])
    O.reverse()

    coeffs = [0]*len(roots)
    for i in range(len(roots)):
        coeffs[i] = divide(-substitute(O,divide(1,a_pow[roots[i]])),substitute(DL,divide(1,a_pow[roots[i]])))
    return coeffs

def get_message(m,roots,coeffs):
    error = [0]*len(m)
    for i in range(len(roots)):
        error[roots[i]] = coeffs[i]
    error.reverse()

    temp = [a_i - b_i for a_i, b_i in zip(m, error)]
    temp = [i%929 for i in temp]
    return temp
