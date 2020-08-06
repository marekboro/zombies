from db.run_sql import run_sql
from models.biting import Biting
from models.human import Human
from models.zombie import Zombie

import repositories.human_repository as human_repository
import repositories.zombie_repository as zombie_repository

def save(biting):
    
    sql = "INSERT INTO bitings (human_id, zombie_id) VALUES (%s,%s) RETURNING id"
    values = [biting.human.id,biting.zombie.id]
    result = run_sql(sql,values)[0]

    biting.id = result['id'] 
    return biting


def select_all():
    bitings = []
    sql = "SELECT * FROM bitings"
    results = run_sql(sql)
    for row in results:
        human = human_repository.select(row["human_id"])
        zombie = zombie_repository.select(row["zombie_id"])
        biting = Biting(human, zombie, row["id"])
        bitings.append(biting)

    return bitings


def select(id):
    biting = None
    sql = "SELECT * FROM bitings WHERE id = %s"
    values = [id]
    result = run_sql(sql,values)[0]

    if result is not None:
        human = human_repository.select(row["human_id"])
        zombie = zombie_repository.select(row["zombie_id"])
        biting = Biting(human, zombie, row["id"])
    
    return biting


def delete(id):
    sql = "DELETE FROM bitings WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def delete_all():
    sql = "DELETE FROM bitings"
    run_sql(sql)

def update(biting):
    sql = "UPDATE bitings SET (human_id, zombie_id) = (%s, %s) WHERE id = %s"
    value = [biting.human.id, biting.zombie.id, biting.id]
    run_sql(sql, value)