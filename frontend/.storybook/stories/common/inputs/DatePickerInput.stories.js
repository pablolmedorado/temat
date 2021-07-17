// Utilities
import { storyFactory } from "../../../util/helpers";
import { boolean, text } from "@storybook/addon-knobs";

// Store
import store from "@/store/index";

// Components
import DatePickerInput from "@/components/inputs/DatePickerInput";

export default { title: "Components/Common/Inputs/DatePickerInput" };

const story = storyFactory({ DatePickerInput });

export const Default = () =>
  story({
    store,
    props: {
      min: {
        default: text("Min date", ""),
      },
      max: {
        default: text("Max date", ""),
      },
      readonly: {
        default: boolean("Read only", false),
      },
    },
    data() {
      return {
        date: new Date().toISOString().split("T")[0],
      };
    },
    template: `
      <DatePickerInput
        v-model="date"
        prepend-icon="mdi-calendar"
        :min="min"
        :max="max"
        :readonly="readonly"
        clearable
      />
    `,
  });
