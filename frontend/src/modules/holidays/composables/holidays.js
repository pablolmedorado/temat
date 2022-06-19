import { ref } from "@vue/composition-api";

import { useMainStore } from "@/stores/main";

import HolidayService from "@/modules/holidays/services/holiday-service";

export function useHolidays() {
  // Store
  const mainStore = useMainStore();

  // State
  const datesToRequest = ref([]);

  // Methods
  async function request() {
    if (
      datesToRequest.value.length &&
      confirm(`¿Confirmas que deseas solicitar estos ${datesToRequest.value.length} días?`)
    ) {
      const response = await HolidayService.request(datesToRequest.value);
      mainStore.showSnackbar({
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
    mainStore.showSnackbar({
      color: "success",
      message: "Día de vacaciones modificado correctamente",
    });
    return response;
  }

  async function cancel(item) {
    if (confirm(`¿Confirmas que deseas cancelar el día de vacaciones con fecha ${item.planned_date}?`)) {
      const response = await HolidayService.cancel(item.id);
      mainStore.showSnackbar({
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
    // State
    datesToRequest,
    // Methods
    request,
    edit,
    cancel,
    getStatusInfo,
  };
}
