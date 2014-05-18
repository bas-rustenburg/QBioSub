rm(list=ls())
locs = read.csv("~/Downloads/StationEntrances.csv")
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
locs$connected[c(160, 1214:1216, 1218)] = "DN"
locs$connected[396] = "ACJLZ" # previously "ACJL"
locs$connected[522] = "BDFM" # previously "7BDFM"
locs$connected[552:553] = "FGR" # previously "F"
locs$connected[785] = "23ACE" # previously "123ACE"
locs$connected[1467] = "EFMR" # previously "eFMR"
locs$connected[c(285, 1279:1281)] = "1AC" # previously "AC"

locs$key = ""
# rule
# connectivity of 4 or more lines: ignore station names
# else: station name plus line connectivity
# exception
# 2- or 3-line crossing station with different names
# DN (New Utrecht Av and 62nd St)
# 6EM (Lexington Av-53rd St and 51st St)
# FG (9th St and Smith-9th St)
# FGR (9th St and Smith-9th St) 4 av
# 1AC (168th St - Washington Heights and 168th St)
# 4-line crossing station but needs disambiguation
# ABCD (125th St and 145th St)
for (j in 1:nrow(locs)) {
  if (nchar(locs$connected[j]) >= 4 | locs$connected[j] == "DN" | locs$connected[j] == "6EM" | locs$connected[j] == "FGR" | locs$connected[j] == "1AC") {
    locs$key[j] = locs$connected[j]
  } else {
    locs$key[j] = paste(locs$Station_Name[j], locs$connected[j], sep="-")
  }
  
  if (locs$connected[j] == "ABCD") {
    locs$key[j] = paste(locs$Station_Name[j], locs$connected[j], sep="-")
  }
}

locs.coord = aggregate(cbind(Station_Latitude, Station_Longitude) ~ key, data=locs, function(a) mean(a))




abcd.junctions = locs[locs$connected == "ABCD", c(1:5, 31)]
large.junctions = locs[nchar(locs$connected) >= 4, c(1:5, 31)]
large.junctions[order(large.junctions$connected), ]
three.junctions = locs[nchar(locs$connected) == 3, c(1:5, 31)]
three.junctions[order(three.junctions$connected), ]
two.junctions = locs[nchar(locs$connected) == 2, c(1:5, 31)]
two.junctions[order(two.junctions$connected), ]
one.junctions = locs[nchar(locs$connected) == 1, c(1:5, 31)]
one.junctions[order(one.junctions$connected), ]


#37, Union Square => 14th St-Union Square
#53-56, Lawrence St => Jay St - MetroTech
#551, Smith-9thSt => 9th St
"Lexington Av-53rd St" => ""


#522, "7BDFM" => "BDFM"
#1467, "eFMR" => "EFMR"
#785, "123ACE" => "23ACE"

#396, ACJL => ACJLZ
