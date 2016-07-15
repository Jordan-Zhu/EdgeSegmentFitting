
function [LineFeature,LPP] = Lseg_to_Lfeat_v2(ListSegLine,ListEdge,imgsize)

% description: it makes a feature vector for each line and also provide the
% index (linear index) for the points which are belonged to that line in matrix LPP

% change since last version is : in the last version LPP  included sub
% index, but in this version it includes linear index

c0 = 1  ;

for cc=1:length(ListSegLine)
    temp1 =  ListSegLine{cc} ;
    [ax,~]= size(temp1);
    
    for c2=1:ax-1
        y1 = temp1(c2,1)     ;
        y2 = temp1(c2+1,1)   ;
        x1 = temp1(c2,2)     ;
        x2 = temp1(c2+1,2)   ;
        m = (y2-y1)/(x2-x1)  ;
        lind1 = sub2ind(imgsize,y1,x1);
        lind2 = sub2ind(imgsize,y2,x2);
        
        L = sqrt((x2-x1)^2+(y2-y1)^2);
        alpha = atand(-m) ;
        
        LineFeature(c0,:) = [y1 x1 y2 x2 L m alpha c0 lind1 lind2] ; % start point/end point/length/slope/angle/number/label
        
        sty = find([ListEdge{cc}(:,1)]==y1) ;
        stx = find([ListEdge{cc}(:,2)]==x1) ; % find the star
        a = intersect (stx,sty) ;
        
        sty = find([ListEdge{cc}(:,1)]==y2) ;
        stx = find([ListEdge{cc}(:,2)]==x2) ;
        b = intersect (stx,sty) ;
        ListPoint{c0} = ListEdge{cc}(a:b,:) ; % each cell of this matrix includes all the edge points on the corresponding line
        
        c0 = c0+1 ;
        if c0>2
            if ((lind1==LineFeature(c0-2,9))&&(lind2==LineFeature(c0-2,10))) % to check if it is a same line as previous, then jumps to next
                c0 = c0-1 ;
            end
            
        end
        
        
        
    end
end

lx = length(ListPoint) ;
Lpp = cell(lx,1) ;

for cnt3=1:lx
    LPP{cnt3,1} = sub2ind(imgsize,ListPoint{cnt3}(:,1),ListPoint{cnt3}(:,2)) ;
end



end