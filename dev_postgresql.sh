#!/usr/bin/env bash
function wait_for_postgresql_running {
    for i in {1..20}
    do
        net="$(docker exec --tty -u postgres postgresql-image pg_ctl status)"
        if [[ $net == *'server is running (PID: '* ]]; then
            echo 'Postgresql is running'
            break
        fi
        echo 'Postgresql not yet running. Waiting for ' $((2*$i)) ' seconds.'
        sleep 2
    done
}

docker run --name=postgresql-image -d  -p 5432:5432 postgres:9.3
wait_for_postgresql_running
docker exec -u postgres:postgres --tty --interactive postgresql-image bash -c "createdb dev"
echo 'Created `dev` database'