import ast
from badges.models import Badge, UserBadge
from missions.models import UserMission

def evaluate_dynamic_badges(user):
    """Evalua las condiciones de laos badges y otorga los que correspondan al usuario."""
    context = {
        "level": user.level,
        "xp": user.xp,
        "missions_completed": UserMission.objects.filter(user=user).count(),
        # Se pueden agregar mas metricas aquí en el futuro para comparar
    }

    for badge in Badge.objects.all():
        if not UserBadge.objects.filter(user=user, badge=badge).exists():
            try:
                if safe_eval(badge.condition_expression, context):
                    UserBadge.objects.create(user=user, badge=badge)

            except Exception:
                continue


def safe_eval(expression, context):
    """Evalua de forma segura una expresión de condición simple."""
    allowed_names = context.copy()
    tree = ast.parse(expression, mode="eval")

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id not in allowed_names:
                raise ValueError(f"Nombre no permitido: {node.id}")
        elif isinstance(node, (ast.Call, ast.Import, ast.ImportFrom)):
            raise ValueError("Operación no permitida")

    return eval(compile(tree, filename="", mode="eval"), {"__builtins__": {}}, allowed_names)
