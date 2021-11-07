import TruncatedText from "@/components/TruncatedText";

export default {
  title: "Components/Common/TruncatedText",
  component: TruncatedText,
  args: {
    value:
      "Lorem fistrum llevame al sircoo diodeno apetecan llevame al sircoo. A gramenawer te va a hasé pupitaa benemeritaar la caidita ese que llega condemor hasta luego Lucas la caidita se calle ustée te voy a borrar el cerito mamaar.",
    textLength: 30,
  },
};

const Template = (args, { argTypes }) => ({
  components: { TruncatedText },
  props: Object.keys(argTypes),
  template: `
    <TruncatedText v-bind="$props" />
  `,
});

export const Default = Template.bind({});

export const Slot = Template.bind({});
Slot.template = `
  <TruncatedText :text-length="textLength">{{ value }}</TruncatedText>
`;
