import TagLabels from "@/components/TagLabels";

export default {
  title: "Components/Common/TagLabels",
  component: TagLabels,
  args: {
    tags: ["Tag 1", "Tag 2", "Tag with length > 20 characters"],
  },
};

const Template = (args, { argTypes }) => ({
  components: { TagLabels },
  props: Object.keys(argTypes),
  template: `
    <TagLabels v-bind="$props" />
  `,
});

export const Default = Template.bind({});
