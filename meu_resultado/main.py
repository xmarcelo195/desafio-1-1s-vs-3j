from fastapi import FastAPI, Request
import json
from datetime import datetime
from collections import Counter

app = FastAPI()
with open(r"src\usuarios_1000.json", encoding='utf-8') as f:
    app.all_users = json.load(f)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users")
async def get_body(request: Request):
    start_time = datetime.now()
    app.all_users = []
    app.all_users.extend(await request.json())
    end_time = datetime.now()
    elapsed_time = (end_time - start_time)
    return {
        "descricao": "Envia o arquivo JSON de usuários para ser carregado na memória.",
        "timestamp": start_time,
        "elapsed_time": elapsed_time,
        "users": app.all_users,
        "response": {
            "status": 200,
            "body": {
                "message": "Usuário adicionado com sucesso!",
                "user_count": len(app.all_users)
                }
            }
        }

@app.get("/users")
def read_root():
    start_time = datetime.now()
    end_time = datetime.now()
    elapsed_time = (end_time - start_time)
    return len(app.all_users)

@app.get("/superusers")
def get_super_users():
    start_time = datetime.now()
    super_users = [user for user in app.all_users if user.get("score", False)>900 and user.get("ativo", False) == True]
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds() * 1000
    return {
        "descricao": "Retorna os usuários com score >= 900 e ativos, com tempo de execução.",
        "response": {
            "status": 200,
            "body": {
                "timestamp": start_time,
                "execution_time_ms": elapsed_time,
                "data": super_users
            }
        }
    }

@app.get("/top_countries")
def get_super_users():
    start_time = datetime.now()
    super_users = [user['pais'] for user in app.all_users if user.get("score", False)>900 and user.get("ativo", False) == True]
    top_countries = Counter(super_users).most_common(5)
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds() * 1000
    return {
            "descricao": "Agrupa os superusuários por país e retorna os 5 com mais usuários.",
            "response": {
            "status": 200,
            "body": {
                "timestamp": start_time,
                "execution_time_ms": elapsed_time,
                "countries": [{"pais":item[0],"total":item[1]} for item in top_countries]
                }
            }
        }
    
@app.get("/team_insights")
def get_team_insights():
    start_time = datetime.now()
    grouped = {}
    for member in app.all_users:
        equipe_nome = member.get("equipe",{}).get("nome", None)
        if equipe_nome not in grouped:
            grouped[equipe_nome] = {
                "quantidade_membros": 0,
                "lider": None,
                "projetos_concluidos": 0,
                "membros_ativos": 0
            }

        grouped[equipe_nome]["quantidade_membros"] += 1

        if member.get("equipe",{}).get("lider", None):
            grouped[equipe_nome]["lider"] = member.get("nome", None)

        if member.get("ativo", False):
            grouped[equipe_nome]["membros_ativos"] += 1

        for projeto in member.get("equipe",{}).get("projetos", {}):
            if projeto.get("concluido", False):
                grouped[equipe_nome]["projetos_concluidos"] += 1

    teams_output = []
    for equipe_nome, metrics in grouped.items():
        total = metrics["quantidade_membros"]
        active = metrics["membros_ativos"]
        active_percentage = round((active / total) * 100, 1) if total > 0 else 0.0

        teams_output.append({
            "team": equipe_nome,
            "total_members": total,
            "leaders": metrics["lider"],
            "completed_projects": metrics["projetos_concluidos"],
            "active_percentage": active_percentage
        })

    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds() * 1000
    return {
        "descricao": "Retorna estatísticas por equipe com base nos membros, projetos e liderança.",
        "response": {
            "status": 200,
            "body": {
                "timestamp": start_time,
                "execution_time_ms": elapsed_time,
                "teams": teams_output
            }
        }
    }
    
