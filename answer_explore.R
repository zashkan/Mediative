library(ggplot2)

hit_rate=function (x)
{
 return (binom.test(sum(x),length(x),conf=0.99,alternative="greater")$conf.int[1])
}

#Read sample data
dataSet=read.csv("C:/Work/UofA/Job Search/Resume/Submission2/Mediative/Assignment/sample2.csv")
sampleCount=nrow(dataSet)
origCount=40428967

#print count of unique values for all columns
for (i in 1:ncol(dataSet))
{
    print(paste("col", i, ": ", length(unique(dataSet[,i])),sep=''))
}

#estimation of number of unique devices in the database
print((length(unique(dataSet$device_id))/sampleCount)*origCount)

#Aggregation results
dataRate1=as.data.frame(as.list(aggregate(dataSet$click~dataSet$device_type+dataSet$device_conn_type,
                         FUN=function (x) c(hit_rate=hit_rate(x), hit=sum(x),trial=length(x)) )))
dataRate1[order(dataRate1[,3],decreasing = TRUE),]

#Figure 2
qplot(y=dataSet.click.trial, factor(dataSet.device_type), data=dataRate1, geom="bar", stat='identity', fill=factor(dataSet.device_conn_type))


#Figure 3
dataRate1=as.data.frame(as.list(aggregate(dataSet$click~dataSet$device_type+dataSet$device_conn_type+dataSet$banner_pos,
                         FUN=function (x) c(hit_rate=hit_rate(x), hit=sum(x),trial=length(x)) )))
dataRate1[order(dataRate1[,3],decreasing = TRUE),]
qplot(y=dataSet.click.hit_rate, factor(dataSet.banner_pos), data=dataRate1,
                             geom="bar", stat='identity', fill=factor(dataSet.banner_pos),
                             facets=dataSet.device_type~dataSet.device_conn_type,
                             xlab='Device connection type'
                             )

#Temporal analysis
dataSet=transform(dataSet,day=as.numeric(substr(hour,5,6))-20)
dataSet=transform(dataSet,h=as.numeric(substr(hour,7,8)))
dataSet[1:10,]
                       
#Figure 4                 
#different days->hours
dataRate1=as.data.frame(as.list(aggregate(dataSet$click~dataSet$day+dataSet$h,
                FUN=function (x) c(hit_rate=hit_rate(x), hit=sum(x),trial=length(x)) )))
ggplot(data=dataRate1, aes(x=factor(dataSet.h), y=dataSet.click.hit_rate, group=dataSet.day, colour=dataSet.day)
                       ) + geom_line() + geom_point() +facet_grid(. ~ dataSet.day)

#Figure 5                   
dataRate1=as.data.frame(as.list(aggregate(dataSet$click~dataSet$h,
                FUN=function (x) c(hit_rate=hit_rate(x), hit=sum(x),trial=length(x)) )))
ggplot(data=dataRate1, aes(x=dataSet.h, y=dataSet.click.hit_rate)
                       ) + geom_line() + geom_point() 
  
#Figure 6                    
dataRate1=as.data.frame(as.list(aggregate(dataSet$click~dataSet$day,
                FUN=function (x) c(hit_rate=hit_rate(x), hit=sum(x),trial=length(x)) )))
ggplot(data=dataRate1, aes(x=dataSet.day, y=dataSet.click.hit_rate)
                       ) + geom_line() + geom_point()                        
 
#Figure 1                                         
dataSet$site_category <- factor(dataSet$site_category,levels=unique(dataSet$site_category),
  	labels=paste("sc",c(1:length(unique(dataSet$site_category))),sep="")
    )
dataSet$device_type <- factor(dataSet$device_type,levels=unique(dataSet$device_type),
  	labels=c("dev1","dev2","dev3","dev4","dev5"))

qplot(click, data=dataSet, geom="histogram", #fill=dataSet$click,
facets=device_type~site_category,
size=I(3),
xlab="Site Category", ylab="Device Type")

