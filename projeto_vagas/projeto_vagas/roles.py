from rolepermissions.roles import AbstractUserRole


class Empresa(AbstractUserRole):
    available_permissions = {
        "criar_vagas": True,
        "editar_vagas": True,
        "excluir_vagas": True,
        "ver_candidatos": True,
    }


class Candidato(AbstractUserRole):
    available_permissions = {"candidatar_vagas": True}
