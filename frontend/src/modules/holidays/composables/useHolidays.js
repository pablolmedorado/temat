import { ref } from "@vue/composition-api";
import { useActions } from "vuex-composition-helpers";

import HolidayService from "@/modules/holidays/services/holiday-service";

export default function () {
  const { showSnackbar } = useActions(["showSnackbar"]);

  const datesToRequest = ref([]);
  async function request() {
    if (
      datesToRequest.value.length &&
      confirm(`¿Confirmas que deseas solicitar estos ${datesToRequest.value.length} días?`)
    ) {
      const response = await HolidayService.request(datesToRequest.value);
      showSnackbar({
        color: "success",
        message: `Días de vacaciones solicitados correctamente: ${datesToRequest.value.length}`,
      });
      datesToRequest.value = [];
      return response;
    }
    return false;
  }

  async function edit(item, approved) {
    const response = await HolidayService.changeApprovalStatus(item.id, approved);
    showSnackbar({
      color: "success",
      message: "Día de vacaciones modificado correctamente",
    });
    return response;
  }

  async function cancel(item) {
    if (confirm(`¿Confirmas que deseas cancelar el día de vacaciones con fecha ${item.planned_date}?`)) {
      const response = await HolidayService.cancel(item.id);
      showSnackbar({
        color: "success",
        message: "Día de vacaciones cancelado correctamente",
      });
      return response;
    }
    return false;
  }

  function getStatusInfo(status) {
    switch (status) {
      case true:
        return { icon: "mdi-check", colour: "green" };
      case false:
        return { icon: "mdi-cancel", colour: "red" };
      case null:
      default:
        return { icon: "mdi-help", colour: "grey" };
    }
  }

  return {
    datesToRequest,
    request,
    edit,
    cancel,
    getStatusInfo,
  };
}
