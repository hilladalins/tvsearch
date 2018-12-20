<div class="episode">
    <h1>{{result['name']}}</h1>
    <h2>Season {{result['season']}} Ep {{result['number']}}</h2>
    % if result['image']:
        <img src="{{result['image']['original']}}" />
    % else:
        <img src="./images/404.jpg"/>
    % end
    {{!result['summary']}}
</div>