# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
# Modifications Copyright 2020 MatheusCod, juliokiyoshi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A sample plugin to demonstrate dynamic loading."""
########## NEW IMPORT ##########
import random
import mimetypes
from tensorboard.backend import http_util
import pandas as pd
########## NEW IMPORT ##########

import json
import os

from tensorboard.plugins import base_plugin
from tensorboard.util import tensor_util
import werkzeug
from werkzeug import wrappers

from powerboard import metadata

_PLUGIN_DIRECTORY_PATH_PART = "/data/plugin/powerboard/"

class PowerBoard(base_plugin.TBPlugin):
    plugin_name = metadata.PLUGIN_NAME

    def __init__(self, context):
        """Instantiates PowerBoard.

        Args:
        context: A base_plugin.TBContext instance.
        """
        self._multiplexer = context.multiplexer

    def is_active(self):
        """Returns whether there is relevant data for the plugin to process.

        When there are no runs with greeting data, TensorBoard will hide the
        plugin from the main navigation bar.
        """
        return bool(
            self._multiplexer.PluginRunToTagToContent(metadata.PLUGIN_NAME)
        )

    def get_plugin_apps(self):
        return {
            "/index.js": self._serve_js,
            "/data": self._serve_data,
            "/plotgraph": self._serve_plotgraph,
            "/static/*": self._serve_static_file,
            "/tags": self._serve_tags,
            "/greetings": self._serve_greetings
        }

    def frontend_metadata(self):
        return base_plugin.FrontendMetadata(es_module_path="/index.js")

    @wrappers.Request.application
    def _serve_js(self, request):
        del request  # unused
        filepath = os.path.join(os.path.dirname(__file__), "static", "index.js")
        with open(filepath) as infile:
            contents = infile.read()
        return werkzeug.Response(
            contents, content_type="application/javascript"
        )

    @wrappers.Request.application
    def _serve_data(self,request):
        path = request.args.get("tag")
        #df = pd.read_csv(path)
        df = pd.read_csv("./data/ipmi_data.csv") 
        #para ver o pandas dataframe 
        #print(df)
        power = df["Sensor_Reading"].tolist()
        time = df["Time_elapsed"].tolist()
        for i in range(len(time)):
            time[i] = float("{:.5f}".format(time[i]))
        dict = {'x': time, 'y': power}
        contents = json.dumps(dict)
        #return werkzeug.Response(contents, content_type="application/json")
        return http_util.Respond(
            request, contents, content_type='application/json'
        )

    @wrappers.Request.application
    def _serve_plotgraph(self, request):
        #del request
        size = random.randint(10, 15)
        new_dict = {
            "x": [i for i in range(size)],
            "y": [random.randint(0, 20) for i in range(size)]
        }
        contents = json.dumps(new_dict)
        #return werkzeug.Response(contents, content_type="application/json")
        return http_util.Respond(
            request, contents, content_type='application/json'
        )

    @wrappers.Request.application
    def _serve_static_file(self, request):
        """Returns a resource file from the static asset directory.
        Requests from the frontend have a path in this form:
        /data/plugin/example_raw_scalars/static/foo
        This serves the appropriate asset: ./static/foo.
        Checks the normpath to guard against path traversal attacks.
        """
        static_path_part = request.path[len(_PLUGIN_DIRECTORY_PATH_PART) :]
        resource_name = os.path.normpath(
            os.path.join(*static_path_part.split("/"))
        )
        if not resource_name.startswith("static" + os.path.sep):
            return http_util.Respond(
                request, "Not found", "text/plain", code=404
            )

        resource_path = os.path.join(os.path.dirname(__file__), resource_name)
        with open(resource_path, "rb") as read_file:
            mimetype = mimetypes.guess_type(resource_path)[0]
            return http_util.Respond(
                request, read_file.read(), content_type=mimetype
            )

    @wrappers.Request.application
    def _serve_tags(self, request):
        #del request  # unused
        mapping = self._multiplexer.PluginRunToTagToContent(
            metadata.PLUGIN_NAME
        )
        result = {run: {} for run in self._multiplexer.Runs()}
        for (run, tag_to_content) in mapping.items():
            for tag in tag_to_content:
                summary_metadata = self._multiplexer.SummaryMetadata(run, tag)
                result[run][tag] = {
                    "description": summary_metadata.summary_description,
                }
        contents = json.dumps(result, sort_keys=True)
        with open('out.txt', 'w') as f:
            print("mapping:", file=f)
            print(mapping, file=f)
            print()
            print("result:", file=f)
            print(result, file=f)
            print()
            print("contents:", file=f)
            print(contents, file=f)
        #return werkzeug.Response(contents, content_type="application/json")
        return http_util.Respond(
            request, contents, content_type='application/json'
        )

    @wrappers.Request.application
    def _serve_greetings(self, request):
        """Serves greeting data for the specified tag and run.

        For details on how to use tags and runs, see
        https://github.com/tensorflow/tensorboard#tags-giving-names-to-data
        """
        run = request.args.get("run")
        tag = request.args.get("tag")
        if run is None or tag is None:
            raise werkzeug.exceptions.BadRequest("Must specify run and tag")
        try:
            data = [
                tensor_util.make_ndarray(event.tensor_proto)
                .item()
                .decode("utf-8")
                for event in self._multiplexer.Tensors(run, tag)
            ]
        except KeyError:
            raise werkzeug.exceptions.BadRequest("Invalid run or tag")
        contents = json.dumps(data, sort_keys=True)
        #return werkzeug.Response(contents, content_type="application/json")
        return http_util.Respond(
            request, contents, content_type='application/json'
        )
