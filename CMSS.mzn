int: t; %number of attributes
int: k; %maximum size of support set
int: n; %number of positive instances
int: m; %number of negative instances
int: c; %number of atMostOne Constraints

set of int: ATT = 1..t;
set of int: SUP = 1..k;
set of int: POS = 1..n;
set of int: NEG = 1..m;
set of int: CONSTR = 1..c;

array [POS, ATT] of 0..1: omegap;
array [NEG, ATT] of 0..1: omegan;
array [CONSTR] of set of ATT: atMostOne;

array [ATT] of var bool: S; % Variables X_i true if in support set S

%%%%%%%%%%%%% constraint for disjointness of projections of S on omegap and omegan %%%%%%%%%%%%%
constraint forall(i in POS)(
            forall(j in NEG)(
              forall(l in ATT)(
                if S[l]=true then omegap[i,l] != omegan[j,l] endif
              )
            )
           );

%%%%%%%%%%%%% size constraint |S| <= k %%%%%%%%%%%%%
constraint sum(i in ATT)(S[i])>0 /\ sum(i in ATT)(S[i])<=k; 

%%%%%%%%%%%%% constraint for atMostOne %%%%%%%%%%%%%
constraint forall(i in CONSTR)(sum(j in ATT where j in atMostOne[i])(S[j])<=1);

solve satisfy;

output [(if fix(S[i])=true then show(i)++" " else "" endif) | i in ATT] % beautify output