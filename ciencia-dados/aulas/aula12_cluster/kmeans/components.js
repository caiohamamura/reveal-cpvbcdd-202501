// =====================================================
// Reveal reactive state
// =====================================================

const revealState = Vue.reactive({

    step: 0

});

// =====================================================
// Reveal sync
// =====================================================

Reveal.on('fragmentshown', event => {

    revealState.step =
        +event.fragment.dataset.fragmentIndex + 1;

});

Reveal.on('fragmenthidden', event => {

    revealState.step =
        +event.fragment.dataset.fragmentIndex;

});

// =====================================================
// Plotly Figure
// =====================================================

const PlotlyFigure = {

    props: {
        traces: {
            type: Array,
            default: () => []
        },
        layout: Object
    },

    data() {

        return {
            plotReady: false
        };
    },

    watch: {

        traces: {
            deep: true,
            handler() {

                if (!this.plotReady) return;

                Plotly.animate(

                    this.$refs.plot,

                    { data: this.traces },

                    {

                        transition: {

                            duration: 800,
                            easing: 'cubic-in-out'

                        },

                        frame: {

                            duration: 800,
                            redraw: false

                        }

                    }

                );
            }
        }

    },

    mounted() {

        Plotly.newPlot(

            this.$refs.plot,

            this.traces,

            this.layout

        );

        this.plotReady = true;
    },

    template: `

    <div
      ref="plot"
      class="plot"
    ></div>

  `
};
