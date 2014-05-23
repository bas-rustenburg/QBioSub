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
# 36th St (Brooklyn)
locs$connected[71:73] = "DNR" # previously "NR"
# Parkside Av, Beverly Rd, Cortelyou Rd, Av H, Av J, Av M, Av U, Neck Rd
locs$connected[c(98, 100:101, 103:105, 107:108, 1198, 1200:1202, 1761)] = "Q" # previously "BQ"
# Franklin Av - Cs
locs$connected[c(265, 1348)] = "Cs" # previously "As" or "ACs"
# 168th St - Washington Heights
locs$connected[c(285, 1279:1281)] = "1AC" # previously "AC"
# High St
locs$connected[c(367, 1337:1338)] = "AC" # previously "2345ACJZ"
# Kingston-Throop, Ralph Av, Rockaway Av, Liberty Av, Van Siclen Av, Shepherd Av
locs$connected[c(387:388, 391:395, 397:408, 1351:1352, 1355:1356, 1767:1768)] = "C" # previously "AC"
# Broadway Junction-East New York
locs$connected[396] = "ACJLZ" # previously "ACJL"
# 47-50th Sts Rockefeller Center
locs$connected[522] = "BDFM" # previously "7BDFM"
# Smith-9th St
locs$connected[551] = "FG" # previously "FGR"
# 4th Av-9th St
locs$connected[552:553] = "FGR" # previously "F"
# 7th Av, Prospect Park-15 St, Fort Hamilton Parkway, Church Av
locs$connected[c(554:570, 1433:1439)] = "FG" # previously "F"
# Briarwood-Van Wyck Blvd
locs$connected[612:614] = "EF" # previously "F"
# Long Island City-Court Square
locs$connected[c(680, 1848:1849)] = "7EGM" # previously "G"
# Park Place
locs$connected[785] = "23ACE" # previously "123ACE"
# Forest Hills-71st Av
locs$connected[1467] = "EFMR" # previously "eFMR"

# principle: no line branching is allowed
# not modeling:
# 5 train at the rush hour
# Wakefield-241st St, 238th St-Nereid Av, 233rd St, 225th St, 219th St,
# Gun Hill Rd, Burke Av, Allerton Av, Pelham Parkway, Bronx Park East
locs$connected[c(997:1020, 1694:1695)] = "2" # previously "25"
# Lefferts Blvd-bound A train stations
# 104th St-Oxford Av, 111th St-Greenwood Av, Lefferts Blvd
locs = locs[-c(421:426, 1361:1364), ]

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
    locs$key[j] = paste0(";", locs$connected[j])
  } else {
    locs$key[j] = paste(locs$Station_Name[j], locs$connected[j], sep=";")
  }
  
  if (locs$connected[j] == "ABCD") {
    locs$key[j] = paste(locs$Station_Name[j], locs$connected[j], sep=";")
  }
}

# 417 stations
locs.coord = aggregate(cbind(Station_Latitude, Station_Longitude) ~ key, data=locs, function(a) mean(a))
write.table(locs.coord, file="~/Desktop/QBioSub/listOfStationsConverted.txt", sep="\t", row.names=F, quote=F)
