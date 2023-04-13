# ![MuLambda Logo](assets/logo.svg)  MuLambda - A platform for automated machine learning

MuLambda is a serverless platform for automated machine learning, aimed at simplifying the deployment and execution of machine learning models in a serverless environment.
The platform provides a meta representation of machine learning serverless functions that takes model parameters into account, enabling infrastructure transparency for function developers.

## Components

The MuLambda platform is built on top of existing computing middleware and provides the following components:

- *Meta representation of machine learning serverless functions:* MuLambda provides a meta representation of machine learning serverless functions that takes model parameters into account, such as the type of model, the accuracy, or the type of data it operates on.
This enables infrastructure transparency for function developers, keeping the simplicity of the serverless paradigm.
- *Model management infrastructure:* MuLambda includes an emulation layer for Amazon SageMaker, working with local execution tools provided by Amazon.
Multiple storage configurations are analyzed and taken into account, and the utility of interfacing existing storage solutions like Amazon S3 is evaluated.
- *Classification scheme for models:* To enable automatic model selection for functions, MuLambda provides a classification scheme for models, which is used by algorithms of varying complexity to select the most appropriate model for a given task.

## Contributing

Contributions to MuLambda are always welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository.
If you would like to contribute code, please open a pull request.

## Acknowledgments

We would like to thank [netidee](https://www.netidee.at) for providing a stipend for this project.
Their support has made it possible for us to develop MuLambda and explore new directions in serverless machine learning.
We would also like to thank our thesis advisor Dr. Thomas Rausch, for their guidance and feedback throughout the development of this project.
Finally, we would like to thank the open-source community for providing the tools and resources that made this project possible.

## License

MuLambda is licensed under the MIT license. See the LICENSE file for details.

