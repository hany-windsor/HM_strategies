# Mathematical model of sequencing operations in hybrid manufacturing systems

#sets
set N; # number of Manufacturing features
set M; # number of Product variants 
set S; # number of Production strategies
set I; # number of Material types
set J{m in M} default {1..4}; # Set up groups in the variant stage for variant m
set G; # Set up groups in the platform stage
set K; # Sequence orders in the platform stage. 
set Q{M} default {1..18} ; # Sequence orders in the variant stage for variant m
set P; # number of Part setups 
set T; # number of Tool types. 

set KK; # number of Sequence orders platform - 1
set QQ{M} default {1..17}; # number of Sequence orders variants  - 1 
set KKK; # number of Sequence orders platform - 2
set QQQ{M} default {1..16}; # number of Sequence orders variants  - 2
set GG; # number of groups -1



#Parameters 
param D{m in M}; # Demand on variant m 
param B{n in N} default 0; # a binary index that is equal to 1 if feature n is an additive feature and equal 0 if the feature is a subtractive feature
param ST{n in N, p in P} default 0; # cutting time required to process feature n form position o (subtractive manufacturing).
param A{n in N, p in P} default 0; # Additive (build) time required to process feature n from position p (additive manufacturing).
param R{n in N} default 10; # Removal time required for removing feature n from the platform from setup p
param PP{n in N} default 0; # Time needed for a post-processing operation after processing feature n
param E{n in N} default 0; # Time needed for inspecting the part after processing feature n.
param W default 10; # time required to set the part in any clamping position.
param O default 5; # time required to set the part in setup position.
param L default 5; # time required to change the cutting tool.
param H default 5; # time required to change the type of the build material.

param RP{n in N, p in P} default 5; # time required to remove feature n from the platform through setup p.

param U{n in N} default 0; # time needed to cure the part after processing feature n.
param IR{n in N, nn in N} default 0; # a binary matrix that indicates whether the two features n and nn should be processed in one setup.
param SR{n in N, nn in N} default 0; # a binary matrix that indicates whether nn should be sequenced some orders away from feature n.
param PR{n in N, nn in N} default 0; # a binary matrix that indicates whether n is a predecessor of feature nn.
param IO{n in N, p in P} default 0; # a binary matrix that indicates whether an inspection is required if feature f is processed through position p or not.
param CS{n in N} default 0; # a binary matrix that indicates whether the part needs curing after processing feature f.
param PO{n in N, p in P} default 0; # a binary matrix that indicates whether a post-processing operation is required if feature f is processed through position p or not.
param MT{n in N, t in T} default 0; # a binary matrix that indicates whether feature n requires tool t or not.
param BM{n in N, i in I} default 0; # a binary matrix that indicates whether feature n requires material m or not.
param SM{n in N, p in P} default 0; # a binary matrix that indicates whether feature n requires a support material if processed through setup position p.
param FA{n in N, p in P} default 1; # a binary matrix that indicates whether feature n is accessible from position p.
param FH{ N,  S} default 1; # a binary matrix that indicates whether feature n belongs to strategy s.
param FV{n in N, m in M} default 1; # binary parameter to indicate whether feature n is required in variant m.

param NR{n in N} default 1; # binary parameter, equals 1 to indicate that feature n can be removed from the platform and 0 otherwise 

param C_n_P{n in N}; # material cost associated with processing feature n in the platform
param C_n_A{n in N}; # material cost associated with adding feature n to the platform to form a variant
param C_n_R{n in N}; # material cost associated with removing feature n from the platform to form a variant.
param C_Subtractive; # cost per second of processing a subtractive feature
param C_Additive; # cost per second of processing an additive feature
param C_Removal; # cost per second of removing a feature from the platform
param C_Cooling; # cost per second of cooling the part
param C_Postprocessing; # cost per second of post-processing operations
param C_Inspection; # cost per second of inspection operations
param C_Tool_change; # cost per second associated with a tool change
param C_Material_change; # cost per second associated with a build material change
param C_Clamping; # cost per second associated with clamping the part
param C_Setup; # cost per second associated with settin up the part
 

#variables

var alpha{n in N} binary; #1 if feature n is executed in the platform stage, 0 otherwise 
var beta{n in N , m in M} binary; # 1 if feature n is executed on the platform to form variant m, 0 otherwise
var gamma {n in N , m in M} binary; # 1 if feature f is eliminated from the platform to form variant m, 0 otherwise
var epsilon{ s in S} binary; # 1 if manufacturing strategy s is chosen for producing the whole part family, 0 otherwise.
var x{n in N, k in K, p in P} binary; # 1 if feature n is processed in sequence k and through setup p in the platform stage.
var y{n in N, m in M, q in Q[m], p in P} binary;# 1 if feature n is processed in sequence q and through setup p while manufacturing variant m     
var pi{g in G} binary; # 1 if group g is formed in the platform stage.
var zeta{m in M, j in J[m]} binary; # 1 if group j is formed while manufacturing variant m.  
var eta{p in P, g in G} binary; # 1 if setup setup p is assigned to group g in the platform stage.
var sigma{m in M, p in P, j in J[m] } binary; # 1 if setup setup p is assigned to group j while manufacturing variant m.  
var rho{k in K, g in G} binary; # 1 if sequence order k is assigned to group g in the platform stage.
var theta{m in M, q in Q[m], j in J[m]} binary; # 1 if sequence order q is assigned to group j while manufacturing variant m
var omega{n in N} binary; # 1 if feature n calls for a curing time in the platform stage.
var mu{n in N, m in M} binary; # 1 if feature n calls for a curing time while manufacturing variant m.
var lambda{n in N} binary; # 1 if feature n calls for a postprocessing operation in the platform stage.
var phi{n in N, m in M} binary; # 1 if feature n calls for a postprocessing operation while manufacturing variant m.       
var nu{n in N} binary; # 1 if feature n calls for an inspection operation in the platform stage.
var tau{n in N, m in M} binary; # 1 if feature n calls for an inspection operation while manufacturing variant m.
var N_T_P{n in N} integer; # Number of times the tool type changes to type t in the platform stage.
var N_T_V{t in T, m in M} integer; # Number of times the tool type changes to type t while manufacturing variant m. 
var N_M_P{i in I} integer; # Number of times the build material type changes to type i in the platform stage.
var N_M_V{i in I, m in M} integer; # Number of times the build material type changes to type i while manufacturing variant m.

var LV1{k in K,g in G,n in N,p in P} >= 0; # linearizing_rho_times_x
var LV2{n in N,m in M,j in J[m],q in Q[m],p in Q[m]} >= 0; # linearizing_theta_times_y
var LV3{n in N,p in P,k in K,nn in N,pp in P,kl in K} >= 0; # linearizing_x_times_x
var LV4{n in N,m in M,q in Q[m],p in P,nn in N,qq in Q[m]}>= 0; # linearizing_y_times_y


# Objective Function
minimize cost: sum{n in N} C_n_P[n]* alpha[n]* sum{m in M} D[m] + sum{n in N, m in M} C_n_A[n] * D[m] * beta[n,m]+ sum{n in N, m in M} C_n_R[n] * D[m] * gamma[n,m] 

+ C_Subtractive * (sum{ m in M} D[m]* sum{ n in N, p in P, k in K : B[n]=0} ST[n,p]* x[n,k,p] + sum{n in N, p in P, m in M,  q in Q[m]: B[n]=0} D[m] * ST[n,p]* y[n,m,q,p])

+ C_Additive * (sum{ m in M} D[m]* sum{n in N, p in P, k in K : B[n]=1} A[n,p]* x[n,k,p] + sum{n in N, p in P,  m in M, q in Q[m] : B[n]=1} D[m] * A[n,p]* y[n,m,q,p]) 

+ C_Removal * (sum{n in N, m in M} D[m] * R[n]* gamma[n,m])

+ C_Cooling * ((sum {m in M, n in N, p in P, k in K : B[n]=1} D[m] *U[n] * x[n,k,p]) + (sum{m in M, n in N, p in P, q in Q[m] :B[n] = 1 } D[m] * U[n] * y[n,m,q,p]))

+ C_Postprocessing * (sum {m in M} D[m] * sum{n in N : B[n]=1} PP[n] * lambda[n] + sum {n in N, m in M:B[n]=1} PP[n] * D[m] * phi[n,m])

+ C_Inspection * (sum {m in M} D[m] * sum{n in N : B[n]=1} E[n] * nu[n] + sum {n in N, m in M:B[n]=1} E[n] * D[m] * tau[n,m])

+ C_Tool_change * L *(sum{t in T} N_T_P[t] + sum{t in T, m in M} N_T_V[t,m])

+ C_Material_change * H *(sum{i in I} N_M_P[i] + sum{i in I, m in M} N_M_V[i,m])

+ C_Setup * O *(sum{g in G} pi[g]+ sum{m in M, j in J[m]} zeta[m,j]);




# Constraints

subject to one_strategy: sum{s in S} epsilon[s] = 1;

subject to either_paltform_or_variant_stage {n in N, m in M}: alpha[n]+ beta[n,m] = sum{s in S} FV[n,m]*FH[n,s] * epsilon[s];

subject to removing_features_in_variant_stage {n in N, m in M, s in S}:  alpha[n] - gamma[n,m] <= FV[n,m];


subject to feature_assignment_to_one_sequence_order_platform {n in N}: sum{p in P, k in K}  x[n,k,p]  = alpha[n];

subject to feature_assignment_to_one_sequence_order_variant{n in N, m in M}: sum{p in P, q in Q[m]} y[n,m,q,p] =  beta[n,m];

subject to sequence_order_assignment_platform {k in K}: sum{n in N, p in P} x[n,k,p] <= 1; # each sequence order is assigend one feature

subject to sequence_order_assignment_variant { m in M, q in Q[m] }: sum{n in N, p in P} y[n,m,q,p] <= 1; # each sequence order is assigend one feature

#subject to avoid_adding_removing_in_vatriant_stage {n in N, m in M, s in S}:  beta[n,m] + gamma[n,m] <= 1;

subject to sequence_order_in_platform {k in K}: sum{g in G} rho[k,g]= 1; # Each sequence order is assigned to only one group in the platform

subject to sequence_order_in_varaint {m in M, q in Q[m]}: sum{j in J[m]} theta[m,q,j]= 1; # Each sequence order is assigned to only one group in the variant stage

subject to one_setup_for_each_paltform_group {g in G}: sum {p in P} eta[p,g] <= 1;

subject to one_setup_for_each_variant_group {m in M, j in J[m]}: sum {p in P} sigma[m,p,j] <= 1;

subject to sequences_assigned_to_formed_groups_platform { g in G} : sum{ k in K} rho[k,g] <= 100 * pi[g];

subject to sequences_assigned_to_formed_groups_variants {m in M, j in J[m]}: sum {q in Q[m]} theta[m,q,j]<= 100* zeta[m,j];


subject to early_sequence_first_platform {k in KK}: sum{n in N, p in P} x[n,k,p] >= sum{n in N, p in P} x[n,k+1,p];

subject to early_sequence_first_variants { m in M, q in QQ[m] }: sum{n in N, p in P} y[n,m,q,p] >= sum{n in N, p in P} y[n,m,q+1,p];

subject to early_group_first_platform {k in KK}: sum{g in G} g * rho[k,g] <= sum{g in G} g * rho[k+1,g];

subject to early_group_first_variants {m in M, q in QQ[m]}: sum{j in J[m]} j * theta[m,q,j] <= sum{j in J[m]} j * theta[m,q+1,j];



subject to accessiblity_to_features_platform_linearized{n in N, p in P, k in K,g in G}: LV1[k,g,n,p] <= FA[n,p] * eta[p,g];

subject to accessiblity_to_features_variants_linearized{m in M, n in N, p in P, q in Q[m], j in J[m]}: LV2[n,m,j,q,p] <= FA[n,p] * sigma[m,p,j];

subject to assigned_order_in_platform {n in N}: sum {k in K, p in P} x[n,k,p] <= alpha[n];

subject to assigned_order_in_variant_stage {m in M, n in N}: sum {q in Q[m], p in P} y[n,m,q,p] <= beta[n,m];

subject to precedence_in_platform {n in N, nn in N, s in S: n<>nn}: 1 + alpha[n] >= PR[n,nn] + alpha[nn];

subject to precdence_relations_in_platform {n in N, nn in N: n<>nn and PR[n,nn] = 1}: sum {k in K, p in P} k * x[n,k,p] <= sum {k in K, p in P} k * x[nn,k,p];

subject to precdence_relations_in_variant_stage {m in M, n in N, nn in N: n<>nn and PR[n,nn] = 1}: sum {q in Q[m], p in P} q* y[n,m,q,p] <= sum {q in Q[m], p in P} q* y[nn,m,q,p];

subject to inclusion_relations_in_platform_linearized {g in G, n in N, nn in N: n<nn and IR[n,nn] = 1}: sum {k in K, p in P} LV1[k,g,n,p] - sum {k in K, p in P} LV1[k,g,nn,p] = 0;

subject to inclusion_relations_in_variant_stage_linearized {m in M, j in J[m], n in N, nn in N: n<nn and IR[n,nn] = 1}: sum {q in Q[m], p in P} LV2[n,m,j,q,p] - sum {q in Q[m], p in P} LV2[nn,m,j,q,p] = 0;

#subject to seclusion_relations_in_platform {k in KKK, n in N, nn in N: n<>nn and SR[n,nn] = 1}: sum {p in P} (x[n,k,p] + x[nn,k+1,p] + x[nn,k+2,p])<= 1;

#subject to seclusion_relations_in_variant_stage {m in M, q in QQQ[m],n in N, nn in N: n<>nn and SR[n,nn] = 1}: sum {p in P} (y[n,m,q,p] + y[nn,m,q+1,p] + y[nn,m,q+2,p]) <= 1  ;


subject to support_material_in_platform_linearized {g in G, p in P, n in N, nn in N: n<nn }: sum {k in K: SM[n,p]=1} LV1[k,g,n,p] - sum {k in K: SM[nn,p]=1} LV1[k,g,nn,p] = 0;

subject to support_material_relations_in_variant_stage_linearized {m in M, j in J[m], p in P,n in N, nn in N: n<nn }: sum {q in Q[m]: SM[n,p]=1} LV2[n,m,j,q,p] - sum {q in Q[m]: SM[nn,p]=1} LV2[nn,m,j,q,p] = 0;

subject to number_of_tool_change_times_in_platform_linearized {t in T}: sum {n in N:B[n] = 0 and MT[n,t]=1}  alpha[n] - sum{n in N, nn in N, p in P, k in KK: B[n] = 0 and n <> nn and MT[n,t] = 1 and MT[nn,t] = 1} LV3[n,p,k,nn,p,k+1] = N_T_P[t];
 
subject to number_of_tool_change_times_in_variant_stage_linearized {m in M, t in T}: sum {n in N:B[n] = 0 and MT[n,t]=1} beta[n,m] - sum{n in N, nn in N, p in P, q in QQ[m]: B[n] = 0 and n <> nn and MT[n,t] = 1 and MT[nn,t] = 1} LV4[n,m,q,p,nn,q+1] = N_T_V[t,m];

subject to number_of_material_change_times_in_platform_linearized {i in I}: sum {n in N:B[n] = 1 and BM[n,i]=1}  alpha[n] - sum{n in N, nn in N, p in P, k in KK: B[n] = 1 and n <> nn and BM[n,i] = 1 and BM[nn,i] = 1} LV3[n,p,k,nn,p,k+1] = N_M_P[i];
 
subject to number_of_material_change_times_in_variant_stage_linearized {m in M, i in I}: sum {n in N:B[n] = 1 and BM[n,i]=1}  beta[n,m] - sum{n in N, nn in N, p in P, q in QQ[m]: B[n] = 1 and n <> nn and BM[n,i] = 1 and BM[nn,i] = 1} LV4[n,m,q,p,nn,q+1] = N_M_V[i,m];

#subject to needs_cooling_in_platform {n in N :B[n] = 1 }: sum {p in P, k in K}  CS[n] * x[n,k,p]  <= omega[n];
 
#subject to needs_cooling_in_variant_stage {n in N, m in M :B[n] = 1 }: sum {p in P, q in Q[m]}  CS[n] * y[n,m,q,p]  <= mu[n,m];

subject to needs_postprocessing_in_platform {n in N :B[n] = 1 }: sum {p in P, k in K}  PO[n,p] * x[n,k,p]  <= lambda[n];
 
subject to needs_postprocessing_in_variant_stage {n in N, m in M :B[n] = 1 }: sum {p in P, q in Q[m]}  PO[n,p] * y[n,m,q,p]  <= phi[n,m];

subject to needs_inspection_in_platform {n in N :B[n] = 1 }: sum {p in P, k in K}  IO[n,p] * x[n,k,p]  <= nu[n];
 
subject to needs_inspection_in_variant_stage {n in N, m in M :B[n] = 1 }: sum {p in P, q in Q[m]}  IO[n,p] * y[n,m,q,p]  <= tau[n,m];


subject to linearizing_rho_times_x_1 {k in K, g in G, n in N, p in P}: LV1[k,g,n,p] >= x[n,k,p] + rho[k,g] - 1;

subject to linearizing_rho_times_x_2 {k in K, g in G, n in N, p in P}: LV1[k,g,n,p] <= x[n,k,p] ;

subject to linearizing_rho_times_x_3 {k in K, g in G, n in N, p in P}: LV1[k,g,n,p] <= rho[k,g] ;


subject to linearizing_theta_times_y_1{n in N, m in M, j in J[m], q in Q[m], p in P}: LV2[n,m,j,q,p] >= y[n,m,q,p] + theta[m,q,j] - 1;

subject to linearizing_theta_times_y_2{n in N, m in M, j in J[m], q in Q[m], p in P}: LV2[n,m,j,q,p] <= y[n,m,q,p];

subject to linearizing_theta_times_y_3{n in N, m in M, j in J[m], q in Q[m], p in P}: LV2[n,m,j,q,p] <= theta[m,q,j];


subject to linearizing_x_times_x_1{n in N, p in P, k in KK, nn in N: n<>nn }: LV3[n,p,k,nn,p,k+1] >= x[n,k,p] + x[nn,k+1,p] - 1;

subject to linearizing_x_times_x_2{n in N, p in P, k in KK, nn in N: n<>nn }: LV3[n,p,k,nn,p,k+1] <= x[n,k,p];

subject to linearizing_x_times_x_3{n in N, p in P, k in KK, nn in N: n<>nn }: LV3[n,p,k,nn,p,k+1] <= x[nn,k+1,p];
 

subject to linearizing_y_times_y_1{n in N, m in M, q in QQ[m], nn in N, p in P}: LV4[n,m,q,p,nn,q+1] >= y[n,m,q,p] + y[nn,m,q+1,p] - 1;

subject to linearizing_y_times_y_2{n in N, m in M, q in QQ[m], nn in N, p in P}: LV4[n,m,q,p,nn,q+1] <= y[n,m,q,p] ;

subject to linearizing_y_times_y_3{n in N, m in M, q in QQ[m], nn in N, p in P}: LV4[n,m,q,p,nn,q+1] <= y[nn,m,q+1,p];
 


#subject to features_manufactured_in_platform {n in N}: alpha[n] <= sum{s in S} FH[n,s] * epsilon[s];
#subject to features_manufactured_in_variant_stage {n in N, m in M}: beta[n,m] <= sum{s in S} FV[n,m]*FH[n,s] * epsilon[s];
#subject to either_paltform_or_variant_stage_linearized {n in N, m in M, s in S}: FH[n,s] * LV5[n,s]+ FH[n,s]* LV6[n,m,s] <= 1;
#subject to feature_assignment_to_one_sequence_order_platform_linearized {n in N, s in S}: sum{p in P, k in K} FH[n,s] * LV8[n,k,p,s] <= 1;
#subject to feature_assignment_to_one_sequence_order_variant_linearized {n in N, m in M, s in S}: sum{p in P, q in Q[m]} FH[n,s] * FV[n,m]* LV9[n,m,q,p,s] = 1;
 