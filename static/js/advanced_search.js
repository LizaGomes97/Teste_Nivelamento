// // static/js/advanced_search.js
const AdvancedSearch = {
  data() {
    return {
      filtroUF: "",
      filtroModalidade: "",
      ordenacao: "razao_social",
      ordemAscendente: true,
      ufsDisponiveis: [],
      modalidadesDisponiveis: [],
    };
  },
  methods: {
    aplicarFiltros() {
      //Emitir evento para componente pai
      this.$emit("filtros-alterados", {
        uf: this.filtroUF,
        modalidade: this.filtroModalidade,
        ordenacao: this.ordenacao,
        ordem: this.ordemAscendente ? "asc" : "desc",
      });
    },

    atualizarOpcoesUnicas(operadoras, todasAsOpcoes = null) {
      // Se recebemos todas as opções, usamos elas
      if (todasAsOpcoes) {
        this.ufsDisponiveis = todasAsOpcoes.ufs;
        this.modalidadesDisponiveis = todasAsOpcoes.modalidades;
        return;
      }

      // Caso contrário, extraímos dos dados atuais
      const ufs = operadoras
        .map((op) => op.UF || op.uf)
        .filter((uf) => uf && uf.trim() !== "")
        .filter((uf, index, self) => self.indexOf(uf) === index)
        .sort();
      this.ufsDisponiveis = ufs;

      const modalidades = operadoras
        .map((op) => op.Modalidade || op.modalidade)
        .filter((m) => m && m.trim() !== "")
        .filter((m, index, self) => self.indexOf(m) === index)
        .sort();
      this.modalidadesDisponiveis = modalidades;
    },
  },

  watch: {
    filtroUF() {
      this.aplicarFiltros();
    },
    filtroModalidade() {
      this.aplicarFiltros();
    },
    ordenacao() {
      this.aplicarFiltros();
    },
    ordemAscendente() {
      this.aplicarFiltros();
    },
  },

  template: `
    <div class="card">
      <div class="card-header">
        <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#filtrosAvancados">
          Filtros Avançados <i class="bi bi-funnel"></i>
        </button>
      </div>
      <div class="collapse" id="filtrosAvancados">
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <label class="form-label">UF</label>
              <select class="form-select" v-model="filtroUF">
                <option value="">Todas</option>
                <option v-for="uf in ufsDisponiveis" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Modalidade</label>
              <select class="form-select" v-model="filtroModalidade">
                <option value="">Todas</option>
                <option v-for="modalidade in modalidadesDisponiveis" :key="modalidade" :value="modalidade">{{ modalidade }}</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Ordenar por</label>
              <select class="form-select" v-model="ordenacao">
                <option value="razao_social">Razão Social</option>
                <option value="nome_fantasia">Nome Fantasia</option>
                <option value="registro_ans">Registro ANS</option>
                <option value="uf">UF</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Ordem</label>
              <select class="form-select" v-model="ordemAscendente">
                <option :value="true">Crescente</option>
                <option :value="false">Decrescente</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
    `,
};
