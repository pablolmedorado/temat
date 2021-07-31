import GroupPill from "@/components/GroupPill";

export default {
  title: "Components/Common/GroupPill",
  component: GroupPill,
  args: {
    group: { name: "Test Group" },
  },
};

const Template = (args, { argTypes }) => ({
  components: { GroupPill },
  props: Object.keys(argTypes),
  template: `
    <GroupPill v-bind="$props" />
  `,
});

export const Default = Template.bind({});
