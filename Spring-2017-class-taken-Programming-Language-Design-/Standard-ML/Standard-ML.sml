"==============1. Exists ==============";
fun exists (x,[]) = false
  | exists (x, y::rest) = if x = y then true else exists (x,rest);

"==============2. ListUnion==============";

fun listUnion (L,[]) = L
  | listUnion (L,(x::rest)) = if exists (x,L) then listUnion (L,rest) else x::(listUnion (L,rest));

"==============3. ListIntersect==============";
fun listIntersect L [] = []
	| listIntersect L (x::rest) = if exists (x,L) then x::(listIntersect L rest) else listIntersect L rest;


"==============4. pairNleft and pairNright==============";
fun splitfirstn n [] = ([],[])
  | splitfirstn 0 L = ([],L)
  | splitfirstn n (x::xs) = let
   val (ux,vx) = splitfirstn (n-1) xs
in
   (x::ux,vx)
end;

fun reverse L = let 
	fun revAppend [] L = L
	| revAppend (x::rest) L = revAppend rest (x::L)
in revAppend L []
end;

fun pairNright n [] = []
  | pairNright n L = let 
  val (ux,vx) = splitfirstn n L
in 
  ux::(pairNright n vx)
end;
fun pairNleft n L =reverse (pairNright n (reverse L));


"==============5. filter (and reverse) ==============";
fun reverse L = let 
	fun revAppend [] L = L
	| revAppend (x::rest) L = revAppend rest (x::L)
in revAppend L []
end;

fun filter pred L = let
   fun revAppFilter pred [] L = L
     | revAppFilter pred (x::rest) L = if pred x then revAppFilter pred rest (x::L) else revAppFilter pred rest L
in
   reverse(revAppFilter pred L [])
end;

"==============6. Merge Sort==============";
"====a) unitList====";
fun unitList L = pairNright 1 L;

"==============7. eitherTree and eitherSearch==============";
"a)";
datatype either = ImAString of string | ImAnInt of int;
"b)";
datatype eitherTree = Leaf of either
   | INTERIOR of (either * eitherTree * eitherTree);
"c)";
fun is x (ImAString _) = false
| is x (ImAnInt i) = (i=x);
fun eitherSearch (Leaf i) x = is x i
  | eitherSearch (INTERIOR (d,t1,t2) ) x= ((eitherSearch t1 x) orelse (eitherSearch t2 x)) orelse (is x d);
"d";
fun eitherTest (node,num,ans) = if (eitherSearch node num) = ans then  true 
                          else  false;

val e1 = ImAnInt 1;
val e2 = ImAnInt 2;
val e3 = ImAnInt 3;
val e4 = ImAnInt 4;
val e5 = ImAnInt 5;
val ea = ImAString "a";
val eb = ImAString "b";
val ec = ImAString "c";
val ed = ImAString "d";
val ee = ImAString "e";
val ef = ImAString "f";
val eg = ImAString "g";
val eh = ImAString "h";
val ei = ImAString "i";
val n31 = INTERIOR (ea,Leaf(e1),Leaf(e1));
val n32 = INTERIOR (eb,Leaf(e2),Leaf(e2));
val n33 = INTERIOR (ec,Leaf(e3),Leaf(e3));
val n34 = INTERIOR (ed,Leaf(e4),Leaf(e4));
val n35 = INTERIOR (ee,Leaf(e5),Leaf(e5));
val n21 = INTERIOR (ef,n31,n32);
val n22 = INTERIOR (eg,n33,n34);
val n11 = INTERIOR (eh,n21,n22);
val n1 = INTERIOR (ei,n11,n35);

"==============8. treeToString==============";
datatype 'a Tree = LEAF of 'a | NODE of ('a Tree) list;

fun treeToString f (LEAF i) = f i
  | treeToString f (NODE j) = String.concat [String.concat ("("::(map (treeToString f) j)),")"];

val L1a = LEAF "a";
val L1b = LEAF "b";
val L1c = LEAF "c";
val L2a = NODE [L1a, L1b, L1c];
val L2b = NODE [L1b, L1c, L1a];
val L3 = NODE [L2a, L2b, L1a, L1b];
val L4 = NODE [L1c, L1b, L3];
val L5 = NODE [L4];
val iL1a = LEAF 1;
val iL1b = LEAF 2;
val iL1c = LEAF 3;
val iL2a = NODE [iL1a, iL1b, iL1c];
val iL2b = NODE [iL1b, iL1c, iL1a];
val iL3 = NODE [iL2a, iL2b, iL1a, iL1b];
val iL4 = NODE [iL1c, iL1b, iL3];
val iL5 = NODE [iL4];
treeToString String.toString L5;
treeToString Int.toString iL5;
"================Test function==============";

fun Test_Exists (n,m,ans) = if exists (n,m) = ans then true else false;
fun Test_ListUnion (n,m,ans) = if listUnion (n,m) = ans then true else false;
fun Test_ListIntersect (n,m,ans) = if  (listIntersect n m) = ans then true else false;
fun Test_pairNright (n,m,ans) = if (pairNright n m) = ans then true else false;
fun Test_pairNleft (n,m,ans) = if (pairNleft n m) = ans then true else false;
fun Test_filter (n, m, ans) = if (filter n m) = ans then true else false;
fun Test_unitList (n,ans) = if (unitList n) =ans then true else false;
fun eitherTest (node,num,ans) = if (eitherSearch node num) = ans then  true 
                          else  false;
fun Test_treeToString (n,m,ans) = if (treeToString n m) = ans then  true 
                          else  false;
" ====Yongjun Chen (ID:11529168) HW 4 ===== ";
"===============Test result==================";
val problem_1_comments = "Comments:The reason of (''a * ''a list) type is because it should support equality testing";
val test1_exists_result = Test_Exists (1,[],false);
val test2_exists_result = Test_Exists (1,[1,2,3],true);
val test3_exists_result = Test_Exists ([1],[[1]],true);
val test4_exists_result = Test_Exists ([1],[[3],[5]],false);
val test5_exists_result = Test_Exists ("c",["b","c","z"],true);
val test1_listunion_result = Test_ListUnion ([1],[1],[1]);
val test2_listunion_result = Test_ListUnion ([1,1,3],[1,2],[2, 1, 1, 3]);
val test3_listunion_result = Test_ListUnion ([[2,3],[1,2]],[[1],[2,3]],[[1], [2, 3], [1, 2]]);
val test1_listintersect_result = Test_ListIntersect([1], [1],[1]);
val test2_listintersect_result = Test_ListIntersect([1,2,3],[1,1,2],[1,1,2]);
val test3_listintersect_result = Test_ListIntersect([[2,3],[1,2],[2,3]],[[1],[2,3]],[[2, 3]]);
val test1_pairNleft_result = Test_pairNleft (2,[1, 2, 3, 4, 5],[[1], [3, 2], [5, 4]]);
val test2_pairNleft_result = Test_pairNleft (3,[1, 2, 3, 4, 5],[[2, 1], [5, 4, 3]]);
val test3_pairNright_result = Test_pairNright (2,[1, 2, 3, 4, 5],[[1, 2], [3, 4], [5]]);
val test4_pairNright_result = Test_pairNright (3,[1, 2, 3, 4, 5],[[1, 2, 3], [4, 5]]);
val test1_filter_result = Test_filter ((fn (x) => (x = 1)),[1,2,3],[1]);
val test2_filter_result = Test_filter ((fn (x) => (x <= 3)),[1,2,3,4],[1, 2, 3]);
val test3_filter_result = Test_filter ((fn (x) => (x <= 2)),[1,2,3,4],[1, 2]);
val test1_unitlist_result = Test_unitList ([],[]);
val test2_unitlist_result = Test_unitList ([1,2,3,4],[[1], [2], [3], [4]]);
val test3_unitlist_result = Test_unitList ([1,2,3,4,5],[[1], [2], [3], [4],[5]]);
val test1_eithersearch_result = eitherTest (n11,1,true);
val test2_eithersearch_result = eitherTest (n1,6,false);
val test3_eithersearch_result = eitherTest (n21,7,false);
val test1_treeToString_result = Test_treeToString (String.toString,L5,"((cb((abc)(bca)ab)))");
val test2_treeToString_result = Test_treeToString (Int.toString,iL5,"((32((123)(231)12)))");
val test3_treeToString_result = Test_treeToString (Int.toString,iL4,"(32((123)(231)12))");






