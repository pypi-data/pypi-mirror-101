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

"""
Página principal de la aplicación.
"""


from flask import Blueprint, render_template
from flask_login import login_required

cacao_app = Blueprint("cacao_app", __name__, template_folder="templates")


@cacao_app.route("/app")
@login_required
def pagina_inicio():
    return render_template("app.html")


def dev_info():
    from cacao_accounting.version import VERSION
    from cacao_accounting.database import DBVERSION

    info = {
        "app": {
            "version": VERSION,
            "dbversion": DBVERSION,
        }
    }
    return info


@cacao_app.route("/development")
def informacion_para_desarrolladores():
    from cacao_accounting.metadata import DEVELOPMENT
    from os import environ

    if DEVELOPMENT or "CACAO_TEST" in environ:
        return render_template("development.html", info=dev_info())
    else:
        from flask import redirect

        return redirect("/login")
