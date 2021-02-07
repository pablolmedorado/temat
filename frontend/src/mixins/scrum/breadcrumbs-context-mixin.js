import EpicService from "@/services/scrum/epic-service";
import SprintService from "@/services/scrum/sprint-service";

import ContextBreadcrumbs from "@/components/scrum/ContextBreadcrumbs";

export default {
  components: { ContextBreadcrumbs },
  props: {
    sprintId: {
      type: String,
      default: null,
    },
    epicId: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      contextItem: null,
    };
  },
  computed: {
    hasContext() {
      return Boolean(this.sprintId || this.epicId);
    },
    context() {
      return { sprint: this.sprintId, epic: this.epicId };
    },
    breadcrumbs() {
      return [];
    },
  },
  provide() {
    return {
      context: this.context,
    };
  },
  watch: {
    context: {
      handler() {
        this.getContext();
      },
      immediate: true,
      deep: true,
    },
  },
  methods: {
    async getContext() {
      let service, pk;
      if (this.sprintId) {
        service = SprintService;
        pk = this.sprintId;
      }
      if (this.epicId) {
        service = EpicService;
        pk = this.epicId;
      }
      if (service && pk) {
        const response = await service.retrieve(pk, { fields: "id,name" });
        this.contextItem = response.data;
      } else {
        this.contextItem = null;
      }
    },
  },
};
