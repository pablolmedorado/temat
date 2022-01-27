import DatePickerInput from "@/components/inputs/DatePickerInput";

export default {
  title: "Components/Common/Inputs/DatePickerInput",
  component: DatePickerInput,
  args: {
    value: new Date().toISOString().split("T")[0],
    label: "Date",
    prependIcon: "mdi-calendar",
    appendIcon: "",
    min: "",
    max: "",
    readonly: false,
    clearable: true,
  },
  argTypes: {
    errorMessages: { table: { disable: true } },
  },
};

const Template = (args, { argTypes }) => ({
  components: { DatePickerInput },
  props: Object.keys(argTypes),
  data() {
    return {
      date: this.value,
    };
  },
  template: `
    <DatePickerInput v-model="date" v-bind="$props" />
  `,
});

export const Default = Template.bind({});
