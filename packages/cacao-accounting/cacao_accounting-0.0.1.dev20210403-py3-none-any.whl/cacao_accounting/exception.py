# Copyright 2020 William José Moreno Reyes
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contributors:
# - William José Moreno Reyes


class CacaoAccountingException(Exception):
    """Clase base para generar errores locales."""


class DataError(CacaoAccountingException):
    """Clase para generar errores de datos."""


class IntegrityError(CacaoAccountingException):
    """Clase para generar errores de Integridad."""


class TransactionError(CacaoAccountingException):
    """Clase para generar errores en transacciones."""


class OperationalError(CacaoAccountingException):
    """Clase para generar errores operativos."""


# <-------------------------------------------------------------------------> #
# Aquí definimos un listado de los mensajes de error utilizados en la aplicacion
ERROR1 = "No se proporcionaron datos."
ERROR2 = "No se ha espeficiado una tabla en la base de datos."
ERROR3 = "Entidad invalida."
ERROR4 = "Cambio de status no valido."
