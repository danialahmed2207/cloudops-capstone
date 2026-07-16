# Remote State: liegt im S3-Bucket statt lokal.
# So teilen sich Laptop und GitHub Actions denselben State,
# und er landet nie im Git-Repo (.tfstate ist in .gitignore).
# use_lockfile: natives S3-Locking (verhindert parallele Läufe).

terraform {
  backend "s3" {
    bucket       = "cloudops-capstone-tfstate-danial-2026"
    key          = "cloudops-capstone/terraform.tfstate"
    region       = "eu-central-1"
    use_lockfile = true
  }
}
