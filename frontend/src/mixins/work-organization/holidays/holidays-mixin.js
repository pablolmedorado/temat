import { mapActions, mapGetters, mapState } from "vuex";
import { DateTime } from "luxon";

import HolidayService from "@/services/work-organization/holiday-service";

const currentDate = DateTime.local();

export default {
  data() {
    return {
      filters: {
        allowance_date__year: currentDate.year,
      },
    };
  },
  computed: {
    ...mapState(["locale", "loggedUser"]),
    ...mapState("users", {
      userOptions: "users",
    }),
    ...mapGetters(["loading", "yearOptions"]),
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    getHolidayStatusRepresentation(status) {
      switch (status) {
        case true:
          return { icon: "mdi-check", colour: "green" };
        case false:
          return { icon: "mdi-cancel", colour: "red" };
        case null:
        default:
          return { icon: "mdi-help", colour: "grey" };
      }
    },
    async cancelHoliday(item) {
      if (confirm(`¿Confirmas que deseas cancelar el día de vacaciones con fecha ${item.planned_date}?`)) {
        await HolidayService.cancel(item.id);
        this.fetchItems();
        this.getSummary();
        this.showSnackbar({
          color: "success",
          message: "Día de vacaciones cancelado correctamente",
        });
      }
    },
  },
};
