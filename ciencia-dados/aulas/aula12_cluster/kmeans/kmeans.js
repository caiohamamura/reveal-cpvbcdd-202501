function initApp() {

  const app = Vue.createApp({

    provide() {

      return {
        revealState
      };
    },

    data() {

      return {

        pointsX: [

          1.0,
          1.5,
          2.0,
          2.2,
          3.2,

          4.8,

          6.5,
          7.2,
          8.0,
          8.5

        ],

        pointsY: [

          1.0,
          1.8,
          1.2,
          2.5,
          3.8,

          5.0,

          6.8,
          7.5,
          8.2,
          7.8

        ],

        c1: {
          x: 2,
          y: 7
        },

        c2: {
          x: 7,
          y: 2
        }

      };
    },

    computed: {

      neutralColors() {

        return Array(
          this.pointsX.length
        ).fill('gray');
      },

      assign1() {

        return assignClusters(

          this.pointsX,
          this.pointsY,

          this.c1,
          this.c2

        );
      },

      move1() {

        return recomputeCentroids(

          this.pointsX,
          this.pointsY,

          this.assign1.assignments

        );
      },

      assign2() {

        return assignClusters(

          this.pointsX,
          this.pointsY,

          this.move1[0],
          this.move1[1]

        );
      },

      move2() {

        return recomputeCentroids(

          this.pointsX,
          this.pointsY,

          this.assign2.assignments

        );
      },

      layout() {

        return {

          title:
            'Composable Plotly',

          paper_bgcolor: '#111',
          plot_bgcolor: '#111',

          font: {
            color: 'white'
          },

          xaxis: {
            range: [0, 10]
          },

          yaxis: {
            range: [0, 10]
          }

        };
      }

    }

  });

  app.component(
    'plotly-figure',
    PlotlyFigure
  );

  app.component(
    'scatter-trace',
    ScatterTrace
  );

  app.component(
    'frame-step',
    FrameStep
  );

  app.mount('#app');

}

// =====================================================
// KMeans helpers
// =====================================================

function assignClusters(

  pointsX,
  pointsY,

  c1,
  c2

) {

  const colors = [];
  const assignments = [];

  for (let i = 0; i < pointsX.length; i++) {

    const d1 =

      (pointsX[i] - c1.x) ** 2 +

      (pointsY[i] - c1.y) ** 2;

    const d2 =

      (pointsX[i] - c2.x) ** 2 +

      (pointsY[i] - c2.y) ** 2;

    if (d1 < d2) {

      colors.push('red');
      assignments.push(0);

    } else {

      colors.push('blue');
      assignments.push(1);
    }
  }

  return {
    colors,
    assignments
  };
}

function recomputeCentroids(

  pointsX,
  pointsY,

  assignments

) {

  let sx1 = 0;
  let sy1 = 0;
  let c1n = 0;

  let sx2 = 0;
  let sy2 = 0;
  let c2n = 0;

  for (let i = 0; i < assignments.length; i++) {

    if (assignments[i] === 0) {

      sx1 += pointsX[i];
      sy1 += pointsY[i];
      c1n++;

    } else {

      sx2 += pointsX[i];
      sy2 += pointsY[i];
      c2n++;
    }
  }

  return [

    {
      x: sx1 / c1n,
      y: sy1 / c1n
    },

    {
      x: sx2 / c2n,
      y: sy2 / c2n
    }

  ];
}