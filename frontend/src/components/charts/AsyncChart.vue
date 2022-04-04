<template>
  <div>
    <highcharts
      v-if="data"
      :key="`${_uid}-${theme}`"
      :constructor-type="constructorType"
      :update-args="[true, true, true]"
      :options="options"
    />
    <v-card v-else :height="height || 400" flat>
      <v-overlay v-if="isLoading" absolute>
        <v-progress-circular indeterminate size="64" />
      </v-overlay>
      <v-alert v-else type="error" text outlined border="left"> Ocurrió un error cargando la gráfica. </v-alert>
    </v-card>
  </div>
</template>

<script>
import { computed, onActivated, ref, watch } from "@vue/composition-api";
import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";

import useLoading from "@/composables/useLoading";

import darkUnica from "@/utils/highcharts/themes/dark-unica-custom";

export const defaultOptions = {
  title: { text: "Análisis" },
  chart: {
    height: 400,
    style: {
      fontFamily: "Roboto",
    },
  },
  credits: { enabled: false },
  exporting: { enabled: true },
  legend: { enabled: true },
  tooltip: {
    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
    pointFormat:
      '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
      '<td style="padding:0"><strong>{point.y:.1f}</strong></td></tr>',
    footerFormat: "</table>",
    shared: true,
    useHTML: true,
  },
  series: [],
};

export default {
  name: "AsyncChart",
  components: {
    highcharts: Chart,
  },
  props: {
    constructorType: {
      type: String,
      default: "chart",
      validator: function (value) {
        return ["chart", "stockChart", "ganttChart"].includes(value);
      },
    },
    optionsFunction: {
      type: Function,
      required: true,
    },
    service: {
      type: Object,
      required: true,
    },
    fetchFunctionName: {
      type: String,
      required: true,
    },
    fetchFunctionArgs: {
      type: Array,
      default: () => [],
    },
    reactiveArgs: {
      type: Boolean,
      default: true,
    },
    height: {
      type: Number,
      default: 400,
    },
  },
  setup(props, { root }) {
    // Composables
    const { isLoading, addTask, removeTask } = useLoading();

    // State
    const data = ref(null);

    // Computed
    const theme = computed(() => (root.$vuetify.theme.isDark ? "dark" : "light"));
    const options = computed(() => {
      const defaultTheme = root.$vuetify.theme.isDark ? darkUnica : Highcharts.getOptions();
      return Highcharts.merge(
        defaultTheme,
        defaultOptions,
        {
          chart: {
            height: props.height,
          },
        },
        props.optionsFunction(data.value)
      );
    });

    // Watchers
    watch(
      () => props.fetchFunctionArgs,
      () => {
        if (props.reactiveArgs) {
          fetchData();
        }
      },
      { deep: true, immediate: true }
    );

    // Methods
    async function fetchData() {
      addTask("fetch-data");
      data.value = null;
      try {
        const response = await props.service[props.fetchFunctionName].apply(props.service, props.fetchFunctionArgs);
        data.value = response.data;
      } finally {
        removeTask("fetch-data");
      }
    }

    // Lifecycle hooks
    onActivated(() => fetchData());

    return {
      // State
      isLoading,
      data,
      // Computed
      theme,
      options,
      // Methods
      fetchData,
    };
  },
};
</script>
