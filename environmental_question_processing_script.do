/*  Note: The data file produced will be at the individual level and cover all ages, irrespective of the variables requested. 
 In this current version of the tool, it is not possible to select variables by wave - though you may edit the code below to do so. */

/****************************************************************************************
* Sample Code for your request:  3edd9dca4a5a42e2bb8f7d5eadf27cc4       *
*****************************************************************************************/
clear all
set more off

// Replace "where" with the filepath of the working folder (where any temporary files created by this programme will be stored)   eg:  c:\ukhls\temp
cd "c:\Users\haoch\Documents\COMP0190\Data\COMP0191-MSc-Project-Code\Temp" 

// Replace "where" with the folderpath where the data has been downloaded and unzipped   eg:   c:\ukhls_data\UKDA-6614-stata\stata\stata13_se\ukhls
global ukhls "c:\Users\haoch\Documents\COMP0190\Data\COMP0191-MSc-Project-Code\UKDA-6614-stata\stata\stata13_se\ukhls"

// Replace "where" with the filepath of the folder where you want to store the final dataset produced by this programme.  eg:  c:\ukhls\results
global outputpath "c:\Users\haoch\Documents\COMP0190\Data\COMP0191-MSc-Project-Code\Stata-Results"

// The file produced by this programme will be named as below. If you want to change the name do it here.
local outputfilename "UKHLS_fine_tuning_responses"

// By default the data will be extracted from the waves whose letter prefixes are written below, and merged. If you want to a different selection of waves, make the change here
local allWaves = "h i j"

// These variables from the indall files will be included. These include some key variables as determined by us PLUS any variables requested by you. 
local indallvars "sex marstat"

// These variables from the indresp files will be included. These include some key variables as determined by us PLUS any variables requested by you. 
local indvars "agegr10_dv qfhigh racel_dv jbnssec_dv urban_dv gor_dv lnprnt vote3 scenv_crlf scenv_bccc scenv_pmep openvb scenv_meds scenv_tlat"

// These variables from the child files will be included. These include some key variables as determined by us PLUS any variables requested by you. 
local chvars ""

// These variables from the hhresp files will be included. These include some key variables as determined by us PLUS any variables requested by you. 
local hhvars "fihhmnlabgrs_dv etariff"

// These variables from the youth files will be included. These include some key variables as determined by us PLUS any variables requested by you. 
local youthvars "age_dv"


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Anything below this line should not be changed! Any changes to the selection of variables and waves, and location of folders, should be made above. //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// this program returns all variable names with the wave prefix
program define getVars, rclass
    version 14.0
	if ("`1'" != "") {
		local wavemyvars = " `1'"
		local wavemyvars = subinstr("`wavemyvars'"," "," `2'_",.)
		local wavemyvars = substr("`wavemyvars'",2,.)
	}
	else local wavemyvars = ""
	return local fixedVars "`wavemyvars'"
end

// this program to returns  which variables exist in this wave
program define getExistingVars, rclass
    version 14.0
	local all = ""
	foreach var in `1' {
		capture confirm variable `var'
		if !_rc {
			local all = "`all' `var'"
		}
	}
	return local existingVars "`all'"
end  

//loop through each wave
foreach wave in `allWaves' {
	// find the wave number
	local waveno=strpos("abcdefghijklmnopqrstuvwxyz","`wave'")

	// find the wave household vars
	getVars "`hhvars'" `wave'
	local wavehhvars = "`r(fixedVars)'"
	
	// find the wave individual vars
	getVars "`indvars'" `wave'
	local waveindvars = "`r(fixedVars)'"
	
	// find the wave all individual vars
	getVars "`indallvars'" `wave'
	local waveindallvars = "`r(fixedVars)'"
	
	// find the wave child vars
	getVars "`chvars'" `wave'
	local wavechvars = "`r(fixedVars)'"
	
	// find the wave youth vars
	getVars "`youthvars'" `wave'
	local waveyouthvars = "`r(fixedVars)'"
	
	// open the the household level file with the required variables
	use "$ukhls/`wave'_hhresp", clear
	getExistingVars "`wave'_hidp `wavehhvars'"
	keep `r(existingVars)'
	
	// if only household variables are required, skip this part and return all households
	if ("`indvars'" != "" || "`chvars'" != "" || "`youthvars'" != "") {
		// if any individual variable is required, first  merge INDALL keeping the pipd (and possibly some default variables?), so that other files can merge on it.
		merge 1:m `wave'_hidp using "$ukhls/`wave'_indall"
		drop _merge
		// drop loose households with no individuals
		drop if (pidp == .)
		
		// keep only variables that were requested and exist in this wave
		getExistingVars "pidp `wave'_hidp `wavehhvars' `waveindallvars'"
		keep `r(existingVars)'
		
		// add any requested individual variables
		if ("`indvars'" != "") {
			merge 1:1 pidp using "$ukhls/`wave'_indresp"
			drop _merge
			// keep only variables that were requested and exist in this wave
			getExistingVars "pidp `wave'_hidp `wavehhvars' `waveindvars' `waveyouthvars' `wavechvars' `waveindallvars'"
			keep `r(existingVars)'
		}
		// add any requested youth variables
		if ("`waveyouthvars'" != "") {
			merge 1:1 pidp using "$ukhls/`wave'_youth"
			drop _merge
			// keep only variables that were requested and exist in this wave
			getExistingVars "pidp `wave'_hidp `wavehhvars' `waveindvars' `waveyouthvars' `wavechvars' `waveindallvars'"
			keep `r(existingVars)'
		}
		// add any requested child variables
		if ("`wavechvars'" != "") {
			merge 1:1 pidp using "$ukhls/`wave'_child"
			drop _merge
			// keep only variables that were requested and exist in this wave
			getExistingVars "pidp `wave'_hidp `wavehhvars' `waveindvars' `waveyouthvars' `wavechvars' `waveindallvars'"
			keep `r(existingVars)'
		}
	}

	// create a wave variable
	gen wavename=`waveno'

	// drop the wave prefix from all variables
	rename `wave'_* *

	// save the file that was created
	save temp_`wave', replace
	
}

// open the file for the first wave (wave a_)
local firstWave = substr("`allWaves'", 1, 1)
use temp_`firstWave', clear

// loop through the remaining waves appending them in the long format
local remainingWaves = substr("`allWaves'", 3, .)

foreach w in `remainingWaves' {
	// append the files for the second wave onwards
	append using temp_`w'
}

// check how many observations are available from each wave
tab wavename

// move pidp to the beginning of the file
order pidp, first

// save the long file
save "$outputpath/`outputfilename'", replace

// erase temporary files
foreach w in `allWaves' {
	erase temp_`w'.dta
}
// $syntax;