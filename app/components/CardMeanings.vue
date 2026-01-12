<script setup lang="ts">
interface Scenario {
  type: 'relationship' | 'business' | 'wealth'
  content: string
}

interface Meaning {
  meaning: string
  keywords: string[]
  summary: string
  scenarios: Scenario[]
}

const model = defineModel<{
  upright: Meaning
  reversed: Meaning
}>({ required: true })

const items = [
  { label: '正位含义', value: 'upright' as const },
  { label: '逆位含义', value: 'reversed' as const }
]

const scenarioTypeOptions = [
  { label: '爱情关系', value: 'relationship' },
  { label: '事业工作', value: 'business' },
  { label: '财务金钱', value: 'wealth' }
]

const addScenario = (position: 'upright' | 'reversed') => {
  model.value[position].scenarios.push({
    type: 'relationship',
    content: ''
  })
}

const removeScenario = (position: 'upright' | 'reversed', index: number) => {
  model.value[position].scenarios.splice(index, 1)
}
</script>

<template>
  <UCard>
    <template #header>
      <h3 class="text-lg font-semibold">
        含义详解
      </h3>
    </template>

    <UTabs
      :items="items"
      class="w-full"
      default-value="upright"
    >
      <template #content="{ item }">
        <div class="space-y-4 pt-4">
          <UFormField label="关键词">
            <UInputTags

              v-model="model[item.value as 'upright' | 'reversed'].keywords"
              placeholder="输入关键词"
            />
          </UFormField>

          <UFormField label="总结">
            <UTextarea
              v-model="model[item.value as 'upright' | 'reversed'].summary"
              :rows="2"
              placeholder="输入总结"
              class="w-full"
            />
          </UFormField>

          <!-- 场景 -->
          <div class="border-t border-default pt-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="font-medium">
                应用场景
              </h4>
              <UButton
                icon="i-lucide-plus"
                size="sm"
                variant="soft"
                @click="addScenario(item.value as 'upright' | 'reversed')"
              >
                添加场景
              </UButton>
            </div>

            <div class="space-y-3">
              <div
                v-for="(scenario, index) in model[item.value as 'upright' | 'reversed'].scenarios"
                :key="index"
                class="flex flex-col gap-2"
              >
                <div class="flex gap-2">
                  <USelect
                    v-model="scenario.type"
                    :items="scenarioTypeOptions"
                    class="w-full"
                  />
                  <UButton
                    icon="i-lucide-trash-2"
                    color="error"
                    variant="ghost"
                    size="sm"
                    @click="removeScenario(item.value as 'upright' | 'reversed', index)"
                  />
                </div>
                <UTextarea
                  v-model="scenario.content"
                  :rows="5"
                  placeholder="输入场景描述"
                  class="flex-1"
                />
              </div>
            </div>
          </div>
        </div>
      </template>
    </UTabs>
  </UCard>
</template>
