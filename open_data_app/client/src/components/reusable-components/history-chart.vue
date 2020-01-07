<script>
import { Line } from 'vue-chartjs';

export default {
  extends: Line,
  name: 'history-chart',
  props: ['chartData'],
  data() {
    return {
      chartdata: {
        labels: this.chartData.labels,
        datasets: this.chartData.datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  },
};
</script>

<style scoped>

</style>