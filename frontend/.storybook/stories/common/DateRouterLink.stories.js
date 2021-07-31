import DateRouterLink from "@/components/DateRouterLink";

export default {
  title: "Components/Common/DateRouterLink",
  component: DateRouterLink,
  args: {
    date: new Date().toISOString().split("T")[0],
  },
};

const Template = (args, { argTypes }) => ({
  components: { DateRouterLink },
  props: Object.keys(argTypes),
  template: `
    <DateRouterLink v-bind="$props" />
  `,
});

export const Default = Template.bind({});
