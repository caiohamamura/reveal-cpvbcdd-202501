window.app.component("header1", {
  props: ["aula", "titleSize", "title"],
  setup() {
    const count = Vue.ref(0);
    const slots = Vue.useSlots().default?.();

    return { count, slots };
  },
  /*html*/
  template: `
        <div
        style="
          display: grid;
          grid-template-rows: 75% 25%;
          height: 700px;
        "
      >
        <!-- r1: Top section -->
        <div
          style="
            background: url('img/fundo.png') no-repeat center/cover;
            display: grid;
            grid-template-rows: auto 1fr auto;
          "
        >
          <!-- Top bar -->
          <div
            style="
              display: flex;
              justify-content: space-between;
              margin: 30px 30px 0 30px;
            "
          >
            <span style="font-size: 24pt"></span>
            <span style="font-size: 24pt">Aula {{ aula }}</span>
          </div>
          <!-- Images middle -->
          <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 0 30px;
              "
            >
            <div v-for="slot in slots" >
              <component :is="slot" style="max-height:260px;" />
            </div>
          </div>
    
          <!-- Bottom heading -->
          <h3
            style="
              margin: 0 30px 60px 30px;
              align-self: end;
            "
            :style="{fontSize: (titleSize || 40) +  'pt'}"
          >
            {{title}}
          </h3>
        </div>
    
        <!-- r2: Bottom info bar -->
        <div
          style="
            display: grid;
            grid-template-columns: 1fr auto;
            align-items: center;
            margin: 0 30px 64px 30px;
          "
        >
          <div style="text-align: left;"
           :style="{fontSize: '27px'}">
            <p>Prof. Caio Hamamura</p>
            <p>hamamura.caio@ifsp.edu.br</p>
          </div>
          <img src="img/Artboard 1 copy 2.png" height="135" alt="" />
        </div>
      </div>
      `,
});
