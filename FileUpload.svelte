<script lang="ts">
  import { file, fileName, resetAnalysis } from '$lib/stores';

  let dragover = $state(false);
  let fileInput: HTMLInputElement;

  function handleFile(f: File) {
    if (!f.name.toLowerCase().endsWith('.pdf')) {
      alert('Please upload a PDF file');
      return;
    }
    if (f.size > 5 * 1024 * 1024) {
      alert('File must be under 5MB');
      return;
    }
    file.set(f);
    fileName.set(f.name);
    resetAnalysis();
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    dragover = false;
    const f = e.dataTransfer?.files[0];
    if (f) handleFile(f);
  }

  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    dragover = true;
  }

  function handleDragLeave() {
    dragover = false;
  }

  function handleInputChange(e: Event) {
    const target = e.target as HTMLInputElement;
    const f = target.files?.[0];
    if (f) handleFile(f);
  }

  function handleClick() {
    fileInput?.click();
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }

  function removeFile() {
    file.set(null);
    fileName.set('');
    resetAnalysis();
    if (fileInput) fileInput.value = '';
  }
</script>

<div class="space-y-2">
  <label class="block text-sm font-medium text-zinc-300" for="resume-upload">
    Resume (PDF)
  </label>

  {#if $fileName}
    <div class="flex items-center gap-3 rounded-lg border border-emerald-500/30 bg-emerald-500/5 px-4 py-3">
      <svg class="h-5 w-5 shrink-0 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <span class="flex-1 truncate text-sm text-zinc-200">{$fileName}</span>
      <button
        onclick={removeFile}
        class="rounded p-1 text-zinc-400 transition-colors hover:bg-zinc-700 hover:text-zinc-200"
        aria-label="Remove file"
      >
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  {:else}
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      class="group relative cursor-pointer rounded-lg border-2 border-dashed transition-all duration-200 {dragover
        ? 'border-amber-400 bg-amber-400/5'
        : 'border-zinc-600 hover:border-zinc-400 hover:bg-zinc-800/50'}"
      role="button"
      tabindex="0"
      ondrop={handleDrop}
      ondragover={handleDragOver}
      ondragleave={handleDragLeave}
      onclick={handleClick}
      onkeydown={handleKeydown}
      aria-label="Upload resume PDF. Click or drag and drop."
    >
      <div class="flex flex-col items-center gap-2 py-8">
        <svg
          class="h-8 w-8 text-zinc-500 transition-colors group-hover:text-zinc-300 {dragover ? 'text-amber-400' : ''}"
          fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
        <p class="text-sm text-zinc-400">
          <span class="font-medium text-zinc-300">Drop your resume here</span> or click to browse
        </p>
        <p class="text-xs text-zinc-500">PDF only, max 5MB</p>
      </div>
    </div>
  {/if}

  <input
    bind:this={fileInput}
    type="file"
    id="resume-upload"
    accept=".pdf"
    class="hidden"
    onchange={handleInputChange}
  />
</div>
