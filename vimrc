source $VIMRUNTIME/defaults.vim
colorscheme molokai
set number
set relativenumber
set ignorecase
set smartcase
set smarttab
set mouse=ic
inoremap jk <esc>
nnoremap gj j
nnoremap gk k
nnoremap j gj
nnoremap k gk
nnoremap <leader>qq :2close<CR>
set autoindent
syntax on
filetype plugin indent on
set t_Co=256
" Tab stuff
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab
set title

:let g:netrw_dirhistmax = 0


"" no more xmllint requests
let g:syntastic_xml_checkers = []
let g:syntastic_docbk_checkers = []
let g:syntastic_xslt_checkers = []

"" Colors {{{


"Diff stuff
if &diff
    set norelativenumber
    "colorscheme vimdiffTraffic
    "colorscheme apprentice
endif

"" changes flags like --this {
hi Special ctermfg=81

"" cursorline
set cursorline
hi CursorLineNr cterm=none ctermfg=green ctermbg=234


"" statusline
hi StatusLine ctermfg=9 ctermbg=0
hi WildMenu ctermfg=black cterm=bold ctermbg=10
hi StatusLineNC ctermfg=grey ctermbg=black
set laststatus=1

set cm=blowfish2

"" Plugin stuff
""- vim-voom settings
let g:voom_python_versions = [3,2]

""- Settings for python syntax checker
let g:syntastic_python_checkers = ['python']
let g:syntastic_python_python_exec = 'python3'


" Backups {{{
set undodir=/tmp// " undo files
set backupdir=/tmp// " backups
"}}}


"" Execute while in python script
" Bind F5 to save file if modified and execute python script in a buffer.
"nnoremap <silent> <F5> :call SaveAndExecutePython()<CR><C-w>w
nnoremap <silent> <leader>ee :call SaveAndExecutePython()<CR><C-w>w
"vnoremap <silent> <F5> :<C-u>call SaveAndExecutePython()<CR>
vnoremap <silent> <leader>rr :<C-u>call SaveAndExecutePython()<CR>

function! SaveAndExecutePython()
    " SOURCE [reusable window]: https://github.com/fatih/vim-go/blob/master/autoload/go/ui.vim

    " save and reload current file
    silent execute "update | edit"

    " get file path of current file
    let s:current_buffer_file_path = expand("%")

    let s:output_buffer_name = "Python"
    let s:output_buffer_filetype = "output"

    " reuse existing buffer window if it exists otherwise create a new one
    if !exists("s:buf_nr") || !bufexists(s:buf_nr)
        silent execute 'botright new ' . s:output_buffer_name
        let s:buf_nr = bufnr('%')
    elseif bufwinnr(s:buf_nr) == -1
        silent execute 'botright new'
        silent execute s:buf_nr . 'buffer'
    elseif bufwinnr(s:buf_nr) != bufwinnr('%')
        silent execute bufwinnr(s:buf_nr) . 'wincmd w'
    endif

    silent execute "setlocal filetype=" . s:output_buffer_filetype
    setlocal bufhidden=delete
    setlocal buftype=nofile
    setlocal noswapfile
    setlocal nobuflisted
    setlocal winfixheight
    setlocal cursorline " make it easy to distinguish
    setlocal nonumber
    setlocal norelativenumber
    setlocal showbreak=""

    " clear the buffer
    setlocal noreadonly
    setlocal modifiable
    %delete _

    " add the console output
    silent execute ".!python3 " . shellescape(s:current_buffer_file_path, 1)

    " resize window to content length
    " Note: This is annoying because if you print a lot of lines then your code buffer is forced to a height of one line every time you run this function.
    "       However without this line the buffer starts off as a default size and if you resize the buffer then it keeps that custom size after repeated runs of this function.
    "       But if you close the output buffer then it returns to using the default size when its recreated
    execute 'resize' . line('$')

    " make the buffer non modifiable
    setlocal readonly
    setlocal nomodifiable
endfunction


"" Execute while in ruby script
nnoremap <silent> <leader>rr :call SaveAndExecuteRuby()<CR><C-w>w
"vnoremap <silent> <leader>rr :<C-u>call SaveAndExecuteRuby()<CR>

function! SaveAndExecuteRuby()
    " SOURCE [reusable window]: https://github.com/fatih/vim-go/blob/master/autoload/go/ui.vim

    " save and reload current file
    silent execute "update | edit"

    " get file path of current file
    let s:current_buffer_file_path = expand("%")

    let s:output_buffer_name = "Ruby"
    let s:output_buffer_filetype = "output"

    " reuse existing buffer window if it exists otherwise create a new one
    if !exists("s:buf_nr") || !bufexists(s:buf_nr)
        silent execute 'botright new ' . s:output_buffer_name
        let s:buf_nr = bufnr('%')
    elseif bufwinnr(s:buf_nr) == -1
        silent execute 'botright new'
        silent execute s:buf_nr . 'buffer'
    elseif bufwinnr(s:buf_nr) != bufwinnr('%')
        silent execute bufwinnr(s:buf_nr) . 'wincmd w'
    endif

    silent execute "setlocal filetype=" . s:output_buffer_filetype
    setlocal bufhidden=delete
    setlocal buftype=nofile
    setlocal noswapfile
    setlocal nobuflisted
    setlocal winfixheight
    setlocal cursorline " make it easy to distinguish
    setlocal nonumber
    setlocal norelativenumber
    setlocal showbreak=""

    " clear the buffer
    setlocal noreadonly
    setlocal modifiable
    %delete _

    " add the console output
    silent execute ".!ruby " . shellescape(s:current_buffer_file_path, 1)

    " resize window to content length
    " Note: This is annoying because if you print a lot of lines then your code buffer is forced to a height of one line every time you run this function.
    "       However without this line the buffer starts off as a default size and if you resize the buffer then it keeps that custom size after repeated runs of this function.
    "       But if you close the output buffer then it returns to using the default size when its recreated
    execute 'resize' . line('$')

    " make the buffer non modifiable
    setlocal readonly
    setlocal nomodifiable
endfunction

" Wayland clipboard
"nnoremap <leader>tt :call system("wl-copy -n", @")<CR>
"xnoremap <leader>tt :call system("wl-copy -n", @")<CR>
"xnoremap <leader>tt :w !wl-copy -n<CR>
