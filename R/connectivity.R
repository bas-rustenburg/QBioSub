# from listOfLines.txt to connectivityNetwork.txt

# load
lines_information = read.delim("~/Desktop/QBioSub/listOfLines.txt", row.names=1, header=F)

# keep only those things after ;
connectivity.1 = gsub("^.*;", "", as.matrix(lines_information))
# collapse stations' entries in each line
connectivity.2 = apply(connectivity.1, 1, function(a) paste0(a, collapse=""))
# split strings by each character
connectivity.3 = sapply(connectivity.2, function(a) strsplit(a, ""))
# remove duplicates and sort
connectivity.4 = lapply(connectivity.3, function(a) sort(unique(a)))

# save
f = file("~/Desktop/QBioSub/connectivityNetwork.txt", "a")
for (j in 1:length(connectivity.4)) {
  cat("line", file=f)
  cat(names(connectivity.4[j]), file=f)
  cat(" = [\"", file=f)
  writeLines(unlist(connectivity.4[j]), con=f, sep="\",\"")
  cat("\"]\n", file=f)
}
close(f)
