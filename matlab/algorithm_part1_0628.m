

%% *******SECTION 1*******

% REMOVE OUT OF ZONE DATA, FILL THE ZEROS, FILTER OUT OF RANGE DATA
Id1 = Id_o(P.zone(1):P.zone(2) , P.zone(3):P.zone(4)) ;
Id2 = Id1 ;
Id3 = zeros(size(Id_o)) ; Id3(P.zone(1):P.zone(2) , P.zone(3):P.zone(4)) = Id2 ;
Id3(Id3<P.lld)= 0 ; Id3(Id3>P.hhd)= 0 ; Id = Id3 ; 

% FIND DEPTH DICOUNTINUTIES
[BW20,~] = edge(Id,'canny',P.thresh_dis); 

% FIND CURVATURE DISCOUNTINUTIES
[Gx, Gy] = imgradientxy(Id);
[Gmag, Gdir] = imgradient(Gx, Gy);
[BW30,~] = edge(Gdir,'canny',P.thresh_curve); 

L00 = label2rgb(fix(Id_o));
L11 = label2rgb(fix(Id));
L22 = label2rgb(fix(180+Gdir));

clear Gx Gy Id1 Id2 Id3

%% *******SECTION 2*******

% SEGMENT AND LABEL THE CURVATURE LINES (CONVEX/CONCAVE)
DE10  = morpho_modify(BW30) ;
[ListEdgeC, ~,~ ] = edgelink(DE10, P.tol_edge); %
ListSegLineC = lineseg(ListEdgeC, P.tol_line); %
[LineFeatureC,ListPointC] = Lseg_to_Lfeat_v2(ListSegLineC,ListEdgeC,size(Id)) ; %LineFeature(c0,:) = [y1 x1 y2 x2 L m alpha c0 lind1 lind2]
[Line_newC,ListPoint_newC,Line_merged_nC] = merge_lines_v3(LineFeatureC,ListPointC,P.thresh_m, size(Id)) ; % merge broken lines
[Line_newC] = LabelLineCurveFeature_v2(Id,Line_newC,ListPoint_newC,P) ; % label the lines (/max/min)


% DROP THE CONVEX LINES AND MAKE A NEW LOGICAL IMAGE
ind1 = find(Line_newC(:,11)==13) ; 
ptn = [] ; 
for mt=1:length(ind1)
ptn = [ptn ; ListPoint_newC{ind1(mt)}(:)] ; 
end
BWn = false(size(Id)) ;
BWn(ptn) = true ; 

% APPLY OR OPERATION TO THE PROCESSED LOGICAL IMAGES FROM DISC. AND CURV.
DE_o = or(BWn,BW20) ;
DE3  = morpho_modify(DE_o) ;

% clear ListEdgeC ListSegLineC LineFeatureC ListPointC Line_newC ListPoint_newC
% clear mt ind1 ptn

%% *******SECTION 3*******

% SEGMENT AND LABEL THE COMBINED IMAGE (DISC./CURV.)
[ListEdge,~, ~ ] = edgelink(DE3, P.tol_edge); %
ListSegLine = lineseg(ListEdge, P.tol_line); %
[LineFeature,ListPoint] = Lseg_to_Lfeat_v2(ListSegLine,ListEdge,size(Id)) ; %LineFeature(c0,:) = [y1 x1 y2 x2 L m alpha c0 lind1 lind2]
[Line_new,ListPoint_new,Line_merged_n] = merge_lines_v3(LineFeature,ListPoint,P.thresh_m, size(Id)) ; % merge broken lines
DE1  = morpho_modify(BW20) ;
[Line_new] = LabelLineFeature_v4(Id,DE1,Line_new,P) ;% label the lines (dis/curv)

clear ListEdge ListSegLine DE1

%% *******SECTION 4*******

% SELECT THE DISIRED LINES FROM THE LIST
f1 = find(Line_new(:,11)~=0) ;
LineInteresting = Line_new(f1,:) ;
[~ ,index]  = sort(LineInteresting(:,7)) ;
LineInteresting = LineInteresting(index,:)   ;

% MATCH THE LINES TO GET THE PAIRS
ListPair = line_match_v3(LineInteresting,P) ;

clear index f1


