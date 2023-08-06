// Copyright 2019 The TensorFlow Authors. All Rights Reserved.
// Modifications Copyright 2020 MatheusCod, juliokiyoshi
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================
export async function render() {
 const stylesheet = document.createElement('link');
 stylesheet.rel = 'stylesheet';
 stylesheet.type = 'text/css'
 stylesheet.href = './static/Chart.min.css';
 document.head.appendChild(stylesheet);

 const newChart = document.createElement("canvas");
 newChart.id = "myChart";
 newChart.width = "600";
 newChart.height = "400";
 newChart.style.margin = "auto";
 document.body.appendChild(newChart);

 //const graphData = await fetch('./plotgraph').then((response) => response.json());
 //data2 contem os dados reais adquiridos pelo IPMI
 //const data2= await fetch('./data').then((response)  => response.json());
 const graphData = await fetch('./data').then((response) => response.json());
 //console.log(data2)

 var script = document.createElement('script');
 script.onload = function () {
   //const graphData = await fetch('./plotgraph').then((response) => response.json());
   var ctx = document.getElementById('myChart').getContext('2d')
   // Disable automatic style injection
   Chart.platform.disableCSSInjection = true;
   var myLineChart = new Chart(ctx, {
     type: 'line',
     data: {
       labels: graphData['x'],
       datasets: [{
         label: 'Power Consumption Through Time',
         data: graphData['y'],
          borderColor: 'rgba(132, 132, 255, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: false,
        scales: {
          xAxes: [{
            ticks: {
              beginAtZero: true
            },
            scaleLabel: {
              display: true,
              labelString: 'Time (s)'
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true
          },
            scaleLabel: {
            display: true,
            labelString: 'Power Consumption (W)'
          }
        }]
      }
    }});
 };
 script.src = "./static/Chart.min.js"//"https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js";
 document.head.appendChild(script);

 //createButton();
}

function createButton() {
  var csv=JSON2CSV(data2);
  var encodedUri = encodeURI(csv);
  var link = document.createElement("a");
  link.id = "link";
  link.href='data:text/csv;charset=utf-8,'+escape(csv);
  link.setAttribute("download", "data.csv");
  document.body.appendChild(link);
  var button = document.createElement('button');
  button.textContent='download';
  document.getElementById("link").appendChild(button);
}

function JSON2CSV(object) {
  var array1 = object['x'];
  var array2=object['y'];
  var str = '';
  var line = '';

  // get all distinct keys
  let titles = ["Power(w)", "Time(s)"];
  console.log(titles)

  let htext =  '"' + titles.join('","') + '"';
  console.log('header:', htext);
  // add to str
  str += htext + '\r\n';
  //
  // lines
  for (var i = 0; i < array1.length; i++) {
    var line = '';
    line += ',"' + array1[i] +  '"'+',"' + array2[i] +  '"';
    str += line.slice(1) + '\r\n';
  }
  return str;
}
