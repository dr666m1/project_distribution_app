# introduction
you can plot most of probability distributions in [scipy](https://docs.scipy.org/doc/scipy/reference/stats.html).

# usage
## web app
visit [here](http://140.238.45.16/)

## docker
run the command below.
by `N_CHOICE` environment variable, you can specify the number of probability distributions to plot (default is 3).

```sh
docker container run -p 8501:8501 -e N_CHOICE=5 ghcr.io/dr666m1/probability_distribution_app
```

## helm
run the script below.

```sh
git clone https://github.com/dr666m1/project_probability_distribution_app.git probability_distribution_app
cd probability_distribution_app
kubectl create -f ./namespace.yaml
helm install pdapp -n pdapp ./chart
```

if you want to override default setting,
you can write yaml file like below and specify in `--values` option.

```yaml
docker:
  tag: latest
  image: ghcr.io/dr666m1/probability_distribution_app
  env:
    n_choice: 2
```
