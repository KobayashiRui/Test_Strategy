
"dein----------------------------------------
if !&compatible
  set nocompatible
endif

" reset augroup
augroup MyAutoCmd
  autocmd!
augroup END

" dein settings {{{
" dein自体の自動インストール
let s:cache_home = empty($XDG_CACHE_HOME) ? expand('~/.cache') : $XDG_CACHE_HOME
let s:dein_dir = s:cache_home . '/dein'
let s:dein_repo_dir = s:dein_dir . '/repos/github.com/Shougo/dein.vim'
if !isdirectory(s:dein_repo_dir)
  call system('git clone https://github.com/Shougo/dein.vim ' . shellescape(s:dein_repo_dir))
endif
let &runtimepath = s:dein_repo_dir .",". &runtimepath
" プラグイン読み込み＆キャッシュ作成
let s:toml_file = fnamemodify(expand('<sfile>'), ':h').'/.TOML/dein.toml'
let s:lazy_toml = fnamemodify(expand('<sfile>'), ':h').'/.TOML/dein_lazy.toml'
if dein#load_state(s:dein_dir)
  call dein#begin(s:dein_dir)
  call dein#load_toml(s:toml_file, {'lazy': 0})
  call dein#load_toml(s:lazy_toml,{'lazy': 1})
  call dein#end()
  call dein#save_state()
endif
" 不足プラグインの自動インストール
if has('vim_starting') && dein#check_install()
  call dein#install()
endif
" }}}
filetype plugin indent on
"-------------------------------------------
let g:indent_guides_enable_on_vim_startup = 1
nnoremap <silent><Space><Space>p :PrevimOpen<CR>
"------------------------
"------------------------------------
" neocomplete.vim
"------------------------------------
""Note: This option must set it in .vimrc(_vimrc).  NOT IN .gvimrc(_gvimrc)!
" Disable AutoComplPop.
let g:acp_enableAtStartup = 0
" Use neocomplete.
let g:neocomplete#enable_at_startup = 1
" Use smartcase.
let g:neocomplete#enable_smart_case = 1
" Set minimum syntax keyword length.
let g:neocomplete#sources#syntax#min_keyword_length = 3
let g:neocomplete#lock_buffer_name_pattern = '\*ku\*'
let g:neocomplete#max_list = 10
" Plugin key-mappings.
inoremap <expr><C-g>     neocomplete#undo_completion()
inoremap <expr><C-l>     neocomplete#complete_common_string()

" Recommended key-mappings.
" <CR>: close popup and save indent.
inoremap <silent> <CR> <C-r>=<SID>my_cr_function()<CR>
function! s:my_cr_function()
  " return neocomplete#close_popup() . "\<CR>"
  " For no inserting <CR> key.
  return pumvisible() ? neocomplete#close_popup() : "\<CR>"
endfunction
" <TAB>: completion.
inoremap <expr><TAB>  pumvisible() ? "\<C-n>" : "\<TAB>"
" <C-h>, <BS>: close popup and delete backword char.
inoremap <expr><C-h> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><BS> neocomplete#smart_close_popup()."\<C-h>"
inoremap <expr><C-y>  neocomplete#close_popup()
inoremap <expr><C-e>  neocomplete#cancel_popup()

" Close popup by <Space>.
inoremap <expr><Space> pumvisible() ? neocomplete#close_popup() : "\<Space>"
autocmd FileType python setlocal omnifunc=jedi#completions

if !exists('g:neocomplete#force_omni_input_patterns')
        let g:neocomplete#force_omni_input_patterns = {}
endif

" let g:neocomplete#force_omni_input_patterns.python = '\%([^. \t]\.\|^\s*@\|^\s*from\s.\+import \|^\s*from \|^\s*import \)\w*'
let g:neocomplete#force_omni_input_patterns.python = '\h\w*\|[^. \t]\.\w*'

noremap <F2> :VimFiler -split -simple -winwidth=45 -no-quit<CR>
noremap <F8> :TagbarToggle<CR>
noremap <F9> :TagbarShowTag<CR>

autocmd FileType python setlocal omnifunc=jedi#completions
noremap <F2> :VimFiler -split -simple -winwidth=45 -no-quit<CR>
if !exists('g:neocomplete#force_omni_input_patterns')
        let g:neocomplete#force_omni_input_patterns = {}
endif

syntax on
colorscheme apprentice
set t_Co=256
"jedi_vim setting-------------------------------------------
""autocmd FileType python setlocal omnifunc=jedi#completions
""autocmd FileType python setlocal completeopt-=preview
""let g:jedi#completions_enabled = 0
""let g:jedi#auto_vim_configuration = 0
""let g:jedi#popup_select_first = 0
let g:jedi#popup_on_dot = 0
"-------------------------------------------------------------

"ステータスライン関連---------------
set backspace=indent,eol,start
set statusline=%F
set statusline+=%m
set statusline+=%r
"これ以降右寄せ
set statusline+=%=
set statusline+=(%l,%c)
set statusline+=\ \[%l/%L]\    
set statusline+=[ENC=%{&fileencoding}]
set laststatus=2
"-----------------------------------
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8,iso-2022-jp,euc-jp,sjis
set clipboard=unnamedplus
set noswapfile
set number
"<>もカッコとしてハイライトする
set matchpairs& matchpairs+=<:>
hi clear CursorLine
set autoindent
set expandtab
set tabstop=4
set shiftwidth=4
set hlsearch
"カッコを自動で閉じる
inoremap { {}<Left>
inoremap [ []<Left>
inoremap " ""<Left>
inoremap ' ''<Left>
"inoremap < <><Left>
inoremap ( ()<Left>
inoremap <C-k> <C-x><C-k>
nnoremap <C-l> $
nnoremap <C-h> 0
nnoremap <F3> :noh<CR>
inoremap jj  <ESC>
cnoremap w!! w !sudo tee > /dev/null %<CR>

"ファイルタイプによって辞書を変える------------
augroup fileTypeIndent
    autocmd!
    autocmd BufNewFile,BufRead *.py setlocal dictionary=~/dict/pyword.dict
    autocmd BufNewFile,BufRead *.c setlocal dictionary=~/dict/cword.dict
    autocmd BufNewFile,BufRead *.cpp setlocal dictionary=~/dict/cppword.dict
augroup END
"---------------------------------------------
"
"ペーストが綺麗にできる----------------
if &term =~ "xterm"
    let &t_ti .= "\e[?2004h"
    let &t_te .= "\e[?2004l"
    let &pastetoggle = "\e[201~"

    function XTermPasteBegin(ret)
        set paste
        return a:ret
    endfunction

    noremap <special> <expr> <Esc>[200~ XTermPasteBegin("0i")
    inoremap <special> <expr> <Esc>[200~ XTermPasteBegin("")
    cnoremap <special> <Esc>[200~ <nop>
    cnoremap <special> <Esc>[201~ <nop>
endif
"--------------------------------------------

hi CursorLine term=none cterm=none ctermbg=17
hi MatchParen ctermbg=1
set nocursorline
autocmd InsertEnter * set cursorline
autocmd InsertLeave * set nocursorline
