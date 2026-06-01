param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# Wrapper only: no diagnostic business rules here.
& emacs-a11y doctor @Args
exit $LASTEXITCODE
