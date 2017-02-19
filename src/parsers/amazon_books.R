#BOOK LIST
all_books<-NULL
all_authors<-NULL
all_links<-NULL

for (i in 1:100)
{
    page <- read_html(paste("https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A283155%2Cp_n_publication_date%3A1250227011&page=",i,sep=""))
    
    books <- page %>% 
        html_nodes(".color-variation-title-replacement") %>%
        html_text()
    
    authors <- page %>% 
        html_nodes(".a-spacing-small .a-spacing-none+ .a-spacing-none") %>%
        html_text()
    
    links <- page %>% 
        html_nodes(".s-access-detail-page") %>%
        html_attr("href")
    
    all_books <- c(all_books,books)
    all_links <- c(all_links,links)
    all_authors <- c(all_authors,authors)
}

book_list<-data.frame(book=all_books,author=all_authors,link=all_links)
book_list$book<-as.character(book_list$book)
book_list$author<-as.character(book_list$author)
book_list$link<-as.character(book_list$link)


book_list$id2<-strsplit(book_list[,3],split="/")
book_list$id<-NA
for (i in 1:dim(book_list)[1])
{
    book_list[i,5]<-book_list[[i,4]][6]
}

book_list$id2<-NULL


##SCRAPPING
library(rvest)
data <- data.frame(review=NULL,ranking=NULL,book=NULL)
start <- 0

book_numbers <- 1:1200
page_numbers <- 1:500

for (j in book_numbers)
{
    
    for (number in page_numbers)  
    {
        page <- read_html (paste("https://www.amazon.com/product-reviews/",book_list[j,4],"/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=avp_only_reviews&sortBy=recent&pageNumber=",number,sep=""))
        review_ids <- page %>% 
            html_nodes(".review") %>%
            html_attr("id")
        
        if (length(review_ids)==0)
            break
        
        for (i in 1:length(review_ids))
        {
            data[start+i,1] <- page %>%
                html_node(paste("#",review_ids[i]," .review-text",sep="")) %>%
                html_text()
            
            data[start+i,2] <- page %>%
                html_node(paste("#",review_ids[i]," .a-icon-alt",sep="")) %>%
                html_text()
            
            data[start+i,3] <- paste(book_list[j,1],book_list[j,2],sep=" ")
        }
        start <- start + length(review_ids)
    }
    
}

names(data) <- c("review","ranking","book")

write.table(data,"book_reviews.csv",sep="|",row.names = F)
