
%% merge lines
ListPoint_new = ListPoint ;   % list point
Line_new = LineIn ;   % line feature
[o1 , ~]=size(Line_new) ;
Line_merged_n = cell(o1,1) ;    % creating the list of the line was merged 
for i=1:o1
    Line_merged_n{i} = i ;
end

temp1 = Line_new(:,9:10) ;  % get the line index(pixel location)
Lpt = unique(temp1) ;  % find the unique point of the line segment
Lpt = sort(Lpt) ; % list of the line start and end points
for ii=1:length(Lpt)
    ptx = Lpt(ii) ;  % duplicated point
    [ar , ~] = find(Line_new == ptx) ;% find the location of the lines has the same point
    i1 = length(ar) ; % find how many lines have the same point 
    
    if (i1>1)
        clear M   
        ar = sort(ar) ;
        cnt30 = 1 ;
        for cnt10=1:length(ar)-1
            p1 = ar(cnt10);
            for cnt20 = cnt10+1:length(ar)
                p2 = ar(cnt20) ;
                M(cnt30,:) = [p1 p2] ;   %find combinations of these possible line
                cnt30 = cnt30 +1 ;
            end
        end
        
        [sm,~] = size(M) ;
        cnt3=1 ;
        while (cnt3<sm+1)   %cnt3  line pair going to be processed
            dm = abs(Line_new(M(cnt3,1),7)-Line_new(M(cnt3,2),7)) ; % angles different
            if dm<thresh_m % less than threshold
                B1 = [(Line_new(M(cnt3,1),9))  (Line_new(M(cnt3,1),10))] ;   % line 1
                B2 = [(Line_new(M(cnt3,2),9))  (Line_new(M(cnt3,2),10))] ;   % line 2
                if (length(intersect(B1,B2))<2) % two lines are not exactly same
                    poo = setdiff([B1 B2],ptx) ; % start and end point of the new line
                    alph1 = Line_new(M(cnt3,1),7) ;  
                    alph2 = Line_new(M(cnt3,2),7) ;  % angle of the line1 and line2 are going to be merged
                    L1 = Line_new(M(cnt3,1),:) ;
                    L2 = Line_new(M(cnt3,2),:) ;   %line feature of line1 and line2
                    ind1  = poo(1) ; ind2 = poo(2) ;   % pixel position of new line
                    [y1,x1] = ind2sub(imgsize,ind1) ; [y2,x2] = ind2sub(imgsize,ind2) ; % get the x1 y1 x2 y2 
                    m = (y2-y1)/(x2-x1)  ; % slope of the new line
                    L = sqrt((x2-x1)^2+(y2-y1)^2);% lenth of the new line
                    alpha = atand(-m) ; % angle of the new line
                    if (alpha >= min(alph1,alph2))&&(max(alph1,alph2) >= alpha) % intesection point is in the middle of the new line
                        Line_new(max(M(cnt3,1),M(cnt3,2)),:)=[] ;
                        Line_new(min(M(cnt3,1),M(cnt3,2)),:)=[] ;    %cancel the lines we are already merged from the line feature list
                        jj1 = Line_merged_n{M(cnt3,1)};   
                        jj2 = Line_merged_n{M(cnt3,2)};     % line pair we merged
                        Line_merged_n(max(M(cnt3,1),M(cnt3,2))) = [] ;
                        Line_merged_n(min(M(cnt3,1),M(cnt3,2))) = [] ; %cancel the lines we are already merged from the merged line list 
                        [c0,~] = size(Line_new) ;  
                        Line_new(c0+1,:) = [y1 x1 y2 x2 L m alpha 0 ind1 ind2] ; 
                        % start point/end  point/length/slope/angle/number/label
                        % and append the new line to the line feature list
                        Line_merged_n{c0+1} = [jj1 jj2] ; % append the merged line in the line merged list
                        
                        % merge the ListPoints
                        Lpp1 = ListPoint_new{M(cnt3,1)} ;
                        Lpp2 = ListPoint_new{M(cnt3,2)} ;
                        f1 = find(Lpp1==ind1); f2 = find(Lpp1==ind2);
                        f3 = find(Lpp2==ind1); f4 = find(Lpp2==ind2);
                        
                        if isempty(f1)
                            L_start = Lpp2 ;
                            L_end   = Lpp1 ;
                            if f3>1
                                L_start = flipud(L_start) ;
                            end
                            if f2==1
                                L_end = flipud(L_end) ;
                            end
                            
                        else
                            L_start = Lpp1 ;
                            L_end   = Lpp2 ;
                            if f1>1
                                L_start = flipud(L_start) ;
                            end
                            if f4==1 ;
                                L_end = flipud(L_end) ;
                            end
                            
                            
                        end
                        ListPoint_new(max(M(cnt3,1),M(cnt3,2))) = [] ;
                        ListPoint_new(min(M(cnt3,1),M(cnt3,2))) = [] ;
                        ListPoint_new{c0+1} = [L_start(1:end-1) ; L_end] ;
                        
                        
                        
                        
                        cnt3 = sm+1 ; % in a case, the condition is true, it doesn't check for other pairs
                    else
                        cnt3 = cnt3+1 ;
                       
                        
                    end
                else
                    cnt3 = cnt3+1 ; % count for the next pair
                    
                    
                end
            else
                cnt3 = cnt3+1 ;
            end
            
        end
        
    end
end

[mx,~] = size(Line_new) ; Line_new(:,8) = 1:mx ;

