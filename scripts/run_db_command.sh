# Usage: pass in the DB container ID as the argument

# Set database configurations
export CT_DB_USERNAME=ct_admin
export CT_DB_NAME=geoconnections


cat ./db/2020-08-15_init-db.sql | k3s kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ./db/udaconnect_public_person.sql | k3s kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ./db/udaconnect_public_location.sql | k3s kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"
