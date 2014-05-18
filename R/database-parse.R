rm(list=ls())
locs = read.csv("~/Desktop/QBioSub/StationEntrances.csv")
# we want a single letter for each line
# Franklin shuttle (FS) is changed to small s
# Grand Central shuttle (GS) is changed to large S
for (j in 6:16) {
  locs[, j] = gsub("FS", "s", locs[, j])
  locs[, j] = gsub("GS", "S", locs[, j])
}
# key for connectivity
# removes NAs and whitespaces
# sorts the lines and returns a collapsed vector
locs$connected = apply(locs[, 6:16], 1, function(a) paste(sort(na.omit(gsub("\\s", "", a))), collapse=""))
# correcting MTA's irregularitires
# 4th Av-9th St
locs$connected[552:553] = "FGR" # previously "F"
# Parkside Av, Neck Rd
locs$connected[c(98, 108, 1198)] = "Q" # previously "BQ"
# Franklin Av - Cs
locs$connected[c(265, 1348)] = "Cs" # previously "As" or "ACs"
# Liberty Av
locs$connected[397:400] = "C" # previously "AC"
# 168th St - Washington Heights
locs$connected[c(285, 1279:1281)] = "1AC" # previously "AC"
# Broadway Junction-East New York
locs$connected[396] = "ACJLZ" # previously "ACJL"
# 47-50th Sts Rockefeller Center
locs$connected[522] = "BDFM" # previously "7BDFM"
# Smith-9th St
locs$connected[551] = "FG" # previously "FGR"
# 7th Av, Prospect Park-15 St, Fort Hamilton Parkway, Church Av
locs$connected[c(554:570, 1433:1439)] = "FG" # previously "F"
# Long Island City-Court Square
locs$connected[c(680, 1848:1849)] = "7EGM" # previously "G"
# Park Place
locs$connected[785] = "23ACE" # previously "123ACE"
# Forest Hills-71st Av
locs$connected[1467] = "EFMR" # previously "eFMR"

locs$key = ""
# rule
# connectivity of 4 or more lines: ignore station names
# else: station name plus line connectivity
# exception
# 2- or 3-line crossing station with different names
# 1R (South Ferry and Whitehall St)
# DN (62 St and New Utrecht Av)
# GL (Metropolitan Av and Lorimer St)
# 1AC (168th St - Washington Heights and 168th St)
# 6EM (Lexington Av-53rd St and 51st St)
# FGR (4 Av and 9th St)
# 4-line crossing station but needs disambiguation
# ABCD (125th St and 145th St)
for (j in 1:nrow(locs)) {
  if (nchar(locs$connected[j]) >= 4 | locs$connected[j] == "1R" | locs$connected[j] == "DN" | locs$connected[j] == "GL" | locs$connected[j] == "1AC" | locs$connected[j] == "6EM" | locs$connected[j] == "FGR") {
    locs$key[j] = locs$connected[j]
  } else {
    locs$key[j] = paste(locs$Station_Name[j], locs$connected[j], sep="-")
  }
  
  if (locs$connected[j] == "ABCD") {
    locs$key[j] = paste(locs$Station_Name[j], locs$connected[j], sep="-")
  }
}

locs.coord = aggregate(cbind(Station_Latitude, Station_Longitude) ~ key, data=locs, function(a) mean(a))
