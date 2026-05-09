// =====================================================
// Reveal reactive state
// =====================================================

const revealState = Vue.reactive({

    step: 0

});

// =====================================================
// Reveal sync
// =====================================================

const fragmentMap = {

    step1: 1,
    step2: 2,
    step3: 3,
    step4: 4,
    step5: 5

};

Reveal.on('fragmentshown', event => {

    revealState.step =
        fragmentMap[event.fragment.id];

});

Reveal.on('fragmenthidden', event => {

    revealState.step =
        fragmentMap[event.fragment.id] - 1;

});

// =====================================================
// Plotly Figure
// =====================================================

const PlotlyFigure = {

    props: {
        layout: Object
    },

    data() {

        return {
            traces: [],
            plotReady: false
        };
    },

    provide() {

        return {

            addTrace: trace => {

                const idx =
                    this.traces.findIndex(
                        t => t.uid === trace.uid
                    );

                const isNew = idx < 0;

                if (isNew) {

                    this.traces.push(trace);

                } else {

                    this.traces[idx] = trace;
                }

                if (!this.plotReady || isNew) {

                    this.renderPlot();

                } else {

                    this.animatePlot();
                }
            },

            removeTrace: uid => {

                this.traces =
                    this.traces.filter(
                        t => t.uid !== uid
                    );

                this.renderPlot();
            },

            revealState
        };
    },

    methods: {

        renderPlot() {

            if (!this.plotReady) {

                Plotly.newPlot(

                    this.$refs.plot,

                    this.traces,

                    this.layout

                );

                this.plotReady = true;

            } else {

                Plotly.react(

                    this.$refs.plot,

                    this.traces,

                    this.layout

                );
            }
        },

        animatePlot() {

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

    },

    mounted() {

        Plotly.newPlot(

            this.$refs.plot,

            [],

            this.layout

        );

        this.plotReady = true;
    },

    template: `

    <div>

      <!-- Hidden Vue components -->
      <div style="display:none">
        <slot />
      </div>

      <!-- Actual Plotly target -->
      <div
        ref="plot"
        class="plot"
      ></div>

    </div>

  `
};

// =====================================================
// Scatter Trace
// =====================================================

const ScatterTrace = {

    inject: [
        'addTrace',
        'removeTrace'
    ],

    props: {

        x: Array,
        y: Array,

        color: {
            default: 'gray'
        },

        size: {
            default: 14
        },

        symbol: {
            default: 'circle'
        },

        mode: {
            default: 'markers'
        }

    },

    data() {

        return {

            uid:
                'trace_' +
                Math.random()
                    .toString(36)
                    .slice(2)

        };
    },

    methods: {

        buildTrace() {

            return {

                uid: this.uid,

                x: this.x,
                y: this.y,

                mode: this.mode,
                type: 'scatter',

                marker: {

                    color: this.color,
                    size: this.size,
                    symbol: this.symbol

                }

            };
        },

        refresh() {

            this.addTrace(
                this.buildTrace()
            );
        }

    },

    mounted() {

        this.addTrace(
            this.buildTrace()
        );
    },

    beforeUnmount() {

        this.removeTrace(
            this.uid
        );
    },

    watch: {

        x: {
            deep: true,
            handler() {
                this.refresh();
            }
        },

        y: {
            deep: true,
            handler() {
                this.refresh();
            }
        },

        color: {
            deep: true,
            handler() {
                this.refresh();
            }
        },
        size() {
            this.refresh();
        },

        symbol() {
            this.refresh();
        },


    },

    template: `
    <div
  style="
    position:absolute;
    width:0;
    height:0;
    overflow:hidden;
  "
>
  <slot />
</div>
  `
};

// =====================================================
// Reveal visibility
// =====================================================

const FrameStep = {

    inject: [
        'revealState'
    ],

    props: {
        at: Number
    },

    computed: {

        visible() {

            return (
                this.revealState.step >=
                this.at
            );
        }

    },

    template: `

    <template v-if="visible">
      <slot />
    </template>

  `
};