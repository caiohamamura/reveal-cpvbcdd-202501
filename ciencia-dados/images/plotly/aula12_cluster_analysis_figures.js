const AULA12_SCATTER_INITIAL_TRACES = [
  {
    x: [69, 72, 75, 78, 70, 74, 77, 71, 73, 76, 68, 79, 72, 75, 70, 73, 76, 74, 71, 77, 70, 74, 98, 102, 105, 95, 100, 107, 96, 103, 99, 101, 94, 106, 97, 104, 100, 108, 95, 102, 110, 93, 88, 116],
    y: [70, 73, 71, 76, 69, 74, 77, 72, 75, 70, 74, 76, 91, 94, 89, 96, 92, 95, 93, 98, 90, 97, 72, 75, 78, 70, 74, 79, 73, 76, 71, 77, 69, 75, 92, 95, 90, 98, 94, 96, 99, 91, 84, 104],
    mode: 'markers',
    type: 'scatter',
    name: 'Pessoas',
    marker: { color: '#8be9fd', size: 11, line: { color: '#282a36', width: 1 } },
    hovertemplate: 'Cintura: %{x} cm<br>Entreperna: %{y} cm<extra></extra>'
  }
];

const AULA12_SCATTER_INITIAL_LAYOUT = {
  title: { text: 'Cintura x entreperna: corpos reais, tamanhos discretos', font: { color: '#f8f8f2' } },
  paper_bgcolor: '#282a36',
  plot_bgcolor: '#282a36',
  font: { color: '#f8f8f2' },
  margin: { l: 60, r: 30, t: 60, b: 55 },
  xaxis: { title: 'Cintura (cm)', gridcolor: '#44475a', zerolinecolor: '#6272a4' },
  yaxis: { title: 'Entreperna (cm)', gridcolor: '#44475a', zerolinecolor: '#6272a4' },
  showlegend: false
};

const AULA12_HIERARCHICAL_CLUSTERS_TRACES = [
  {
    x: [69, 72, 75, 78, 70, 74, 77, 71, 73, 76, 68, 79],
    y: [70, 73, 71, 76, 69, 74, 77, 72, 75, 70, 74, 76],
    mode: 'markers',
    type: 'scatter',
    name: 'Baixo/estreito',
    marker: { color: '#8be9fd', size: 11 }
  },
  {
    x: [72, 75, 70, 73, 76, 74, 71, 77, 70, 74],
    y: [91, 94, 89, 96, 92, 95, 93, 98, 90, 97],
    mode: 'markers',
    type: 'scatter',
    name: 'Alto/estreito',
    marker: { color: '#ff79c6', size: 11 }
  },
  {
    x: [98, 102, 105, 95, 100, 107, 96, 103, 99, 101, 94, 106],
    y: [72, 75, 78, 70, 74, 79, 73, 76, 71, 77, 69, 75],
    mode: 'markers',
    type: 'scatter',
    name: 'Baixo/largo',
    marker: { color: '#50fa7b', size: 11 }
  },
  {
    x: [97, 104, 100, 108, 95, 102, 110, 93],
    y: [92, 95, 90, 98, 94, 96, 99, 91],
    mode: 'markers',
    type: 'scatter',
    name: 'Alto/largo',
    marker: { color: '#f1fa8c', size: 11 }
  },
  {
    x: [88, 116],
    y: [84, 104],
    mode: 'markers',
    type: 'scatter',
    name: 'Ambíguos/outliers',
    marker: { color: '#ff5555', size: 13, symbol: 'x' }
  }
];

const AULA12_HIERARCHICAL_CLUSTERS_LAYOUT = {
  title: { text: 'Corte da hierarquia: quatro grupos interpretáveis', font: { color: '#f8f8f2' } },
  paper_bgcolor: '#282a36',
  plot_bgcolor: '#282a36',
  font: { color: '#f8f8f2' },
  margin: { l: 60, r: 30, t: 60, b: 55 },
  xaxis: { title: 'Cintura (cm)', gridcolor: '#44475a' },
  yaxis: { title: 'Entreperna (cm)', gridcolor: '#44475a' },
  legend: { orientation: 'h', y: -0.25 }
};

const AULA12_DENDROGRAM_TRACES = [
  {
    x: [1, 1, 2, 2, null, 3, 3, 4, 4, null, 1.5, 1.5, 3.5, 3.5, null, 6, 6, 7, 7, null, 8, 8, 9, 9, null, 6.5, 6.5, 8.5, 8.5, null, 2.5, 2.5, 7.5, 7.5],
    y: [0, 3, 3, 0, null, 0, 4, 4, 0, null, 3, 12, 12, 4, null, 0, 3, 3, 0, null, 0, 5, 5, 0, null, 3, 14, 14, 5, null, 12, 31, 31, 14],
    mode: 'lines',
    type: 'scatter',
    line: { color: '#8be9fd', width: 4 },
    hoverinfo: 'skip',
    name: 'fusões'
  },
  {
    x: [0.5, 9.5],
    y: [18, 18],
    mode: 'lines',
    type: 'scatter',
    line: { color: '#ff79c6', width: 3, dash: 'dash' },
    name: 'corte sugerido'
  }
];

const AULA12_DENDROGRAM_LAYOUT = {
  title: { text: 'Dendrograma: grandes saltos sugerem cortes naturais', font: { color: '#f8f8f2' } },
  paper_bgcolor: '#282a36',
  plot_bgcolor: '#282a36',
  font: { color: '#f8f8f2' },
  margin: { l: 60, r: 30, t: 60, b: 55 },
  xaxis: { title: 'Pessoas/grupos', showticklabels: false, gridcolor: '#44475a' },
  yaxis: { title: 'Distância da fusão', gridcolor: '#44475a' }
};

const AULA12_KMEANS_STEP_0_TRACES = [
  {
    x: [69, 72, 75, 78, 70, 74, 77, 71, 73, 76, 68, 79, 72, 75, 70, 73, 76, 74, 71, 77, 70, 74, 98, 102, 105, 95, 100, 107, 96, 103, 99, 101, 94, 106, 97, 104, 100, 108, 95, 102, 110, 93],
    y: [70, 73, 71, 76, 69, 74, 77, 72, 75, 70, 74, 76, 91, 94, 89, 96, 92, 95, 93, 98, 90, 97, 72, 75, 78, 70, 74, 79, 73, 76, 71, 77, 69, 75, 92, 95, 90, 98, 94, 96, 99, 91],
    mode: 'markers',
    type: 'scatter',
    name: 'pessoas',
    marker: { color: '#6272a4', size: 10 }
  },
  {
    x: [66, 82, 91, 111],
    y: [68, 101, 68, 100],
    mode: 'markers',
    type: 'scatter',
    name: 'centroides iniciais',
    marker: { color: '#ff5555', size: 18, symbol: 'x', line: { width: 3 } }
  }
];

const AULA12_KMEANS_STEP_1_TRACES = [
  {
    x: [69, 72, 75, 78, 70, 74, 77, 71, 73, 76, 68, 79],
    y: [70, 73, 71, 76, 69, 74, 77, 72, 75, 70, 74, 76],
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 1',
    marker: { color: '#8be9fd', size: 10 }
  },
  {
    x: [72, 75, 70, 73, 76, 74, 71, 77, 70, 74],
    y: [91, 94, 89, 96, 92, 95, 93, 98, 90, 97],
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 2',
    marker: { color: '#ff79c6', size: 10 }
  },
  {
    x: [98, 102, 105, 95, 100, 107, 96, 103, 99, 101, 94, 106],
    y: [72, 75, 78, 70, 74, 79, 73, 76, 71, 77, 69, 75],
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 3',
    marker: { color: '#50fa7b', size: 10 }
  },
  {
    x: [97, 104, 100, 108, 95, 102, 110, 93],
    y: [92, 95, 90, 98, 94, 96, 99, 91],
    mode: 'markers',
    type: 'scatter',
    name: 'cluster 4',
    marker: { color: '#f1fa8c', size: 10 }
  },
  {
    x: [66, 82, 91, 111],
    y: [68, 101, 68, 100],
    mode: 'markers',
    type: 'scatter',
    name: 'centroides',
    marker: { color: ['#8be9fd', '#ff79c6', '#50fa7b', '#f1fa8c'], size: 18, symbol: 'x', line: { color: '#f8f8f2', width: 2 } }
  }
];

const AULA12_KMEANS_STEP_2_TRACES = [
  ...AULA12_KMEANS_STEP_1_TRACES.slice(0, 4),
  {
    x: [73.5, 73.2, 100.5, 101.1],
    y: [73.1, 93.5, 74.1, 94.4],
    mode: 'markers',
    type: 'scatter',
    name: 'novos centroides',
    marker: { color: ['#8be9fd', '#ff79c6', '#50fa7b', '#f1fa8c'], size: 20, symbol: 'x', line: { color: '#f8f8f2', width: 2 } }
  }
];

const AULA12_KMEANS_STEP_3_TRACES = AULA12_KMEANS_STEP_2_TRACES;

const AULA12_KMEANS_LAYOUT = {
  title: { text: 'K-Means: atribuir ao centroide mais próximo e recalcular médias', font: { color: '#f8f8f2' } },
  paper_bgcolor: '#282a36',
  plot_bgcolor: '#282a36',
  font: { color: '#f8f8f2' },
  margin: { l: 60, r: 30, t: 60, b: 55 },
  xaxis: { title: 'Cintura (cm)', range: [60, 116], gridcolor: '#44475a' },
  yaxis: { title: 'Entreperna (cm)', range: [64, 104], gridcolor: '#44475a' },
  legend: { orientation: 'h', y: -0.25 }
};

const AULA12_ELBOW_TRACES = [
  {
    x: [1, 2, 3, 4, 5, 6, 7, 8],
    y: [19100, 9800, 4900, 1850, 1510, 1320, 1190, 1080],
    mode: 'lines+markers',
    type: 'scatter',
    name: 'inércia',
    line: { color: '#50fa7b', width: 4 },
    marker: { color: '#50fa7b', size: 10 }
  }
];

const AULA12_ELBOW_LAYOUT = {
  title: { text: 'Método do cotovelo: ganho marginal ao aumentar k', font: { color: '#f8f8f2' } },
  paper_bgcolor: '#282a36',
  plot_bgcolor: '#282a36',
  font: { color: '#f8f8f2' },
  margin: { l: 60, r: 30, t: 60, b: 55 },
  xaxis: { title: 'Número de clusters (k)', dtick: 1, gridcolor: '#44475a' },
  yaxis: { title: 'Inércia / SSE', gridcolor: '#44475a' },
  shapes: [{ type: 'line', x0: 4, x1: 4, y0: 0, y1: 19100, line: { color: '#ff79c6', dash: 'dash', width: 3 } }]
};

const AULA12_DBSCAN_TRACES = [
  {
    x: [62, 65, 68, 71, 74, 77, 80, 83, 86, 89],
    y: [72, 77, 81, 84, 86, 86, 84, 81, 77, 72],
    mode: 'markers+lines',
    type: 'scatter',
    name: 'grupo curvo',
    marker: { color: '#8be9fd', size: 10 },
    line: { color: '#8be9fd', width: 2 }
  },
  {
    x: [92, 95, 98, 101, 104, 107, 110],
    y: [69, 72, 75, 78, 82, 86, 90],
    mode: 'markers+lines',
    type: 'scatter',
    name: 'grupo alongado',
    marker: { color: '#50fa7b', size: 10 },
    line: { color: '#50fa7b', width: 2 }
  },
  {
    x: [74, 76, 78, 80, 82, 84, 86, 88],
    y: [95, 97, 98, 99, 98, 97, 95, 93],
    mode: 'markers',
    type: 'scatter',
    name: 'grupo denso',
    marker: { color: '#ff79c6', size: 10 }
  },
  {
    x: [58, 116, 101, 67, 112],
    y: [101, 66, 103, 64, 76],
    mode: 'markers',
    type: 'scatter',
    name: 'ruído',
    marker: { color: '#ff5555', size: 14, symbol: 'x' }
  }
];

const AULA12_DBSCAN_LAYOUT = {
  title: { text: 'DBSCAN: regiões densas viram clusters, pontos isolados viram ruído', font: { color: '#f8f8f2' } },
  paper_bgcolor: '#282a36',
  plot_bgcolor: '#282a36',
  font: { color: '#f8f8f2' },
  margin: { l: 60, r: 30, t: 60, b: 55 },
  xaxis: { title: 'Cintura (cm)', gridcolor: '#44475a' },
  yaxis: { title: 'Entreperna (cm)', gridcolor: '#44475a' },
  legend: { orientation: 'h', y: -0.25 }
};
