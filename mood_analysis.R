# -------------------------------------------
# mood_analysis.R
# -------------------------------------------
# This script receives quiz answers as JSON
# and returns a mood label for Django
# -------------------------------------------

# Load required package
if(!require(jsonlite)){
    install.packages("jsonlite", repos='http://cran.us.r-project.org')
    library(jsonlite)
}

# Read arguments (answers JSON)
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
    cat("Neutral")
    quit()
}

answers_json <- args[1]

# Parse JSON into vector
answers <- fromJSON(answers_json)

# Count yes/no
yes_count <- sum(answers == "yes")
no_count  <- sum(answers == "no")

# Basic Mood Logic
if (yes_count >= 5) {
    cat("Excited")
} else if (yes_count >= 3) {
    cat("Neutral")
} else {
    cat("Tired")
}
